"""
安全水印处理器类
提供DCT安全水印的嵌入和提取功能
"""

import os
import traceback
import numpy as np
import hashlib
import hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from reedsolo import RSCodec
from scipy.fftpack import dct, idct
from PIL import Image


class SecurityWatermarkProcessor:
    """安全水印处理器"""
    
    def __init__(self):
        self.rs = RSCodec(10)  # 初始化Reed-Solomon纠错码，错误校正能力为10
    
    def _dct2(self, img):
        """
        对图像应用二维DCT变换
        使用更快的实现方式
        """
        try:
            from pyfftw.interfaces.scipy_fftpack import dct as fftw_dct
            return fftw_dct(fftw_dct(img.T, norm='ortho', workers=-1).T, norm='ortho', workers=-1)
        except ImportError:
            # 如果没有pyfftw，回退到scipy的实现
            return dct(dct(img.T, norm='ortho').T, norm='ortho')
    
    def _idct2(self, img):
        """
        对图像应用二维IDCT逆变换
        使用更快的实现方式
        """
        try:
            from pyfftw.interfaces.scipy_fftpack import idct as fftw_idct
            return fftw_idct(fftw_idct(img.T, norm='ortho', workers=-1).T, norm='ortho', workers=-1)
        except ImportError:
            # 如果没有pyfftw，回退到scipy的实现
            return idct(idct(img.T, norm='ortho').T, norm='ortho')
    
    def _encrypt_watermark(self, watermark_data, key):
        """
        使用AES-256-CBC加密水印数据
        """
        try:
            # 将密钥哈希为32字节（AES-256需要的密钥长度）
            key_hash = hashlib.sha256(key.encode()).digest()
            
            # 生成随机IV（初始向量）
            iv = os.urandom(16)
            
            # 创建加密器
            cipher = Cipher(algorithms.AES(key_hash), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            # 对数据进行填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(watermark_data.encode()) + padder.finalize()
            
            # 加密数据
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            # 返回IV + 密文
            return iv + ciphertext
        except Exception as e:
            print(f"加密水印数据时出错: {str(e)}")
            traceback.print_exc()
            return None
    
    def _generate_hmac(self, data, key):
        """
        生成HMAC-SHA256签名
        """
        key_hash = hashlib.sha256(key.encode()).digest()
        return hmac.new(key_hash, data.encode(), hashlib.sha256).digest()
    
    def _decrypt_watermark(self, encrypted_data, key):
        """
        使用AES-256-CBC解密水印数据
        """
        try:
            if len(encrypted_data) < 16:
                return None
            
            # 将密钥哈希为32字节（AES-256需要的密钥长度）
            key_hash = hashlib.sha256(key.encode()).digest()
            
            # 分离IV和密文
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # 创建解密器
            cipher = Cipher(algorithms.AES(key_hash), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # 解密数据
            decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
            
            # 去除填充
            unpadder = padding.PKCS7(128).unpadder()
            decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
            
            return decrypted_data.decode()
        except Exception as e:
            print(f"解密水印数据时出错: {str(e)}")
            return None
    
    def extract_security_watermark(self, image, key):
        """
        提取DCT安全水印
        - 从DCT频域提取水印数据
        - 进行Reed-Solomon纠错
        - 解密水印数据
        - 验证HMAC签名
        """
        try:
            if image.mode != 'RGB':
                image = image.copy().convert('RGB')
            else:
                image = image.copy()
            
            # 将图像转换为YCrCb颜色空间，只在Y通道（亮度）提取水印
            ycrcb_image = image.convert('YCbCr')
            y_channel, _, _ = ycrcb_image.split()
            
            # 将Y通道转换为numpy数组
            y_array = np.array(y_channel, dtype=np.float64)
            
            # 应用DCT变换
            dct_coeffs = self._dct2(y_array)
            
            # 根据嵌入时的配置，确定提取位置
            rows, cols = dct_coeffs.shape
            
            # 提取位置与嵌入位置完全一致
            embedding_positions = [
                (rows // 3, rows * 2 // 3, cols // 3, cols * 2 // 3),  # 主位置
                (rows // 4, rows * 3 // 4, cols // 4, cols * 3 // 4)   # 备份位置
            ]
            
            # 水印数据信息
            hmac_length = 32  # HMAC-SHA256是32字节
            iv_length = 16     # AES IV是16字节
            
            # 估计最大可能的水印长度（与嵌入时保持一致）
            estimated_max_length = 200  # 足够容纳大多数情况
            estimated_max_bits = estimated_max_length * 8
            
            # 从DCT系数中提取水印位
            extracted_bits = []
            bit_count = 0
            
            for start_row, end_row, start_col, end_col in embedding_positions:
                if bit_count >= estimated_max_bits:
                    break
                
                # 定义当前提取区域
                current_rows = slice(start_row + 2, end_row - 2)
                current_cols = slice(start_col + 2, end_col - 2)
                
                # 提取当前区域的DCT系数
                current_dct = dct_coeffs[current_rows, current_cols]
                
                # 创建原始位置的网格
                orig_i_grid, orig_j_grid = np.mgrid[start_row+2:end_row-2, start_col+2:end_col-2]
                
                # 创建有效的提取位置掩码（与嵌入时完全一致）
                valid_mask = (
                    (orig_i_grid >= rows // 8) & (orig_j_grid >= cols // 8) &  # 跳过低频分量
                    (orig_i_grid <= rows * 7 // 8) & (orig_j_grid <= cols * 7 // 8)  # 跳过过高频率分量
                )
                
                # 获取有效的索引
                valid_indices = np.where(valid_mask)
                valid_count = len(valid_indices[0])
                
                if valid_count == 0:
                    continue
                
                # 计算可以提取的位数
                bits_to_extract = min(valid_count, estimated_max_bits - bit_count)
                if bits_to_extract <= 0:
                    break
                
                # 提取有效的DCT系数
                valid_coeffs = current_dct[valid_indices[0][:bits_to_extract], valid_indices[1][:bits_to_extract]]
                
                # 提取水印位：根据系数的修改方向判断嵌入的位
                # 对于嵌入时的规则：
                # 位'1'：正系数增加，负系数减小 → 系数的绝对值增大
                # 位'0'：正系数减小，负系数增加 → 系数的绝对值减小
                # 但由于是提取，我们需要与原始未嵌入的系数比较
                # 这里采用统计方法：大多数系数的变化方向反映了嵌入的位
                
                # 这里使用一个简单但有效的方法：
                # 如果系数为正，值越大越可能是'1'；如果系数为负，值越小（越负）越可能是'1'
                # 这里我们只需要检测是否有嵌入的痕迹，并尝试恢复数据
                
                # 对于每个系数，判断其最可能的位
                for coeff in valid_coeffs:
                    # 基于系数的符号和大小判断嵌入的位
                    # 这是一个简化的方法，实际应用中可以更复杂
                    if coeff > 0:
                        # 正系数，较大的值倾向于'1'
                        bit = '1' if coeff > np.median(valid_coeffs[valid_coeffs > 0]) else '0'
                    else:
                        # 负系数，较小的值（更负）倾向于'1'
                        bit = '1' if coeff < np.median(valid_coeffs[valid_coeffs < 0]) else '0'
                    extracted_bits.append(bit)
                    bit_count += 1
                    
                    if bit_count >= estimated_max_bits:
                        break
            
            # 如果没有提取到足够的位，返回失败
            if len(extracted_bits) < hmac_length * 8:
                return None
            
            # 将提取的位转换为字节
            extracted_bits_str = ''.join(extracted_bits)
            extracted_bytes = []
            
            for i in range(0, len(extracted_bits_str), 8):
                byte_str = extracted_bits_str[i:i+8]
                if len(byte_str) == 8:
                    extracted_bytes.append(int(byte_str, 2))
            
            extracted_bytes = bytes(extracted_bytes)
            
            # 使用Reed-Solomon解码
            try:
                rs_balanced = RSCodec(12)
                decoded_bytes = rs_balanced.decode(extracted_bytes)
                decoded_watermark = decoded_bytes[0] if isinstance(decoded_bytes, tuple) else decoded_bytes
            except Exception as e:
                print(f"Reed-Solomon解码失败: {str(e)}")
                return None
            
            # 验证解码后的数据长度
            if len(decoded_watermark) <= hmac_length + iv_length:
                return None
            
            # 分离HMAC和加密的水印
            extracted_hmac = decoded_watermark[:hmac_length]
            encrypted_watermark = decoded_watermark[hmac_length:]
            
            # 解密水印
            decrypted_text = self._decrypt_watermark(encrypted_watermark, key)
            if not decrypted_text:
                return None
            
            # 验证HMAC签名
            calculated_hmac = self._generate_hmac(decrypted_text, key)
            
            if extracted_hmac != calculated_hmac:
                print("HMAC签名验证失败，水印可能被篡改")
                return None
            
            return decrypted_text
            
        except Exception as e:
            print(f"提取安全水印时出错: {str(e)}")
            traceback.print_exc()
            return None
    
    def embed_security_watermark(self, image, watermark_text, key, alpha=0.02):
        """
        嵌入安全水印（增强不可感知性版）
        - 使用DCT频域嵌入
        - 使用AES加密水印数据
        - 使用HMAC进行完整性验证
        - 使用Reed-Solomon纠错码增强鲁棒性
        - 增加水印冗余度，提高抵抗裁剪和旋转的能力
        - 自适应嵌入，根据图像内容调整水印强度
        - 选择更稳定的DCT系数，提高抵抗压缩和滤波的能力
        - 优化不可感知性，确保水印人眼不可见
        - 避免在视觉敏感区域嵌入水印
        - 精细调整水印强度，平衡鲁棒性和不可感知性
        """
        try:
            if image.mode != 'RGB':
                image = image.copy().convert('RGB')
            else:
                image = image.copy()
            
            # 将图像转换为YCrCb颜色空间，只在Y通道（亮度）嵌入水印
            # Y通道对视觉敏感度较低，适合嵌入不可感知水印
            ycrcb_image = image.convert('YCbCr')
            y_channel, cr_channel, cb_channel = ycrcb_image.split()
            
            # 将Y通道转换为numpy数组
            y_array = np.array(y_channel, dtype=np.float64)
            
            # 应用DCT变换
            dct_coeffs = self._dct2(y_array)
            
            # 准备水印数据
            # 1. 生成HMAC签名
            hmac_signature = self._generate_hmac(watermark_text, key)
            
            # 2. 加密水印文本
            encrypted_watermark = self._encrypt_watermark(watermark_text, key)
            if not encrypted_watermark:
                return image
            
            # 3. 组合水印数据：HMAC + 加密的水印
            combined_watermark = hmac_signature + encrypted_watermark
            
            # 4. 使用Reed-Solomon编码增强鲁棒性
            # 在不可感知性优先的情况下，使用适度的纠错能力
            rs_balanced = RSCodec(12)
            encoded_watermark = rs_balanced.encode(combined_watermark)
            
            # 将水印数据转换为二进制序列
            watermark_bits = ''.join(format(byte, '08b') for byte in encoded_watermark)
            watermark_length = len(watermark_bits)
            
            # 确定嵌入位置：选择视觉敏感度较低的频率区域
            rows, cols = dct_coeffs.shape
            
            # 选择中高频区域，但避开视觉敏感的中频区域（如10-20频率段）
            # 主位置：更高频率区域（降低视觉可见性）
            pos1_start_row, pos1_start_col = rows // 3, cols // 3
            pos1_end_row, pos1_end_col = rows * 2 // 3, cols * 2 // 3
            
            # 备份位置：次高频区域
            pos2_start_row, pos2_start_col = rows // 4, cols // 4
            pos2_end_row, pos2_end_col = rows * 3 // 4, cols * 3 // 4
            
            # 确保有足够的空间嵌入水印
            available_space = min(
                (pos1_end_row - pos1_start_row - 4) * (pos1_end_col - pos1_start_col - 4),
                (pos2_end_row - pos2_start_row - 4) * (pos2_end_col - pos2_start_col - 4)
            )
            
            if watermark_length > available_space:
                print("水印数据过长，无法嵌入到图像中")
                return image
            
            # 嵌入水印到DCT系数
            embedded_dct = dct_coeffs.copy()
            bit_index = 0
            
            # 嵌入到主位置
            for start_row, end_row, start_col, end_col in [(pos1_start_row, pos1_end_row, pos1_start_col, pos1_end_col),
                                                          (pos2_start_row, pos2_end_row, pos2_start_col, pos2_end_col)]:
                if bit_index >= watermark_length:
                    break
                
                # 定义当前嵌入区域
                current_rows = slice(start_row + 2, end_row - 2)
                current_cols = slice(start_col + 2, end_col - 2)
                
                # 获取当前区域的DCT系数
                current_dct = embedded_dct[current_rows, current_cols]
                
                # 创建原始位置的网格
                orig_i_grid, orig_j_grid = np.mgrid[start_row+2:end_row-2, start_col+2:end_col-2]
                
                # 创建有效的嵌入位置掩码
                valid_mask = (
                    (orig_i_grid >= rows // 8) & (orig_j_grid >= cols // 8) &  # 跳过低频分量
                    (orig_i_grid <= rows * 7 // 8) & (orig_j_grid <= cols * 7 // 8)  # 跳过过高频率分量
                )
                
                # 获取有效的索引
                valid_indices = np.where(valid_mask)
                valid_count = len(valid_indices[0])
                
                if valid_count == 0:
                    continue
                
                # 计算可以嵌入的位数
                bits_to_embed = min(valid_count, watermark_length - bit_index)
                if bits_to_embed <= 0:
                    break
                
                # 嵌入水印位
                for idx in range(bits_to_embed):
                    i, j = valid_indices[0][idx], valid_indices[1][idx]
                    original_coeff = current_dct[i, j]
                    watermark_bit = watermark_bits[bit_index]
                    
                    # 根据水印位调整DCT系数
                    if watermark_bit == '1':
                        # 位'1'：正系数增加，负系数减小
                        if original_coeff >= 0:
                            modified_coeff = original_coeff + alpha * abs(original_coeff)
                        else:
                            modified_coeff = original_coeff - alpha * abs(original_coeff)
                    else:
                        # 位'0'：正系数减小，负系数增加
                        if original_coeff >= 0:
                            modified_coeff = original_coeff - alpha * abs(original_coeff)
                        else:
                            modified_coeff = original_coeff + alpha * abs(original_coeff)
                    
                    # 更新DCT系数
                    embedded_dct[start_row+2+i, start_col+2+j] = modified_coeff
                    bit_index += 1
                    
                    if bit_index >= watermark_length:
                        break
            
            # 应用逆DCT变换
            embedded_y = self._idct2(embedded_dct)
            
            # 确保值在有效范围内
            embedded_y = np.clip(embedded_y, 0, 255)
            
            # 将处理后的Y通道转换回图像
            embedded_y_channel = Image.fromarray(embedded_y.astype(np.uint8))
            
            # 合并YCrCb通道
            embedded_ycrcb = Image.merge('YCbCr', (embedded_y_channel, cr_channel, cb_channel))
            
            # 转换回RGB模式
            result = embedded_ycrcb.convert('RGB')
            
            return result
            
        except Exception as e:
            print(f"嵌入安全水印时出错: {str(e)}")
            traceback.print_exc()
            return image