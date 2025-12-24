#!/usr/bin/env python3
"""
测试重构后的GUI模块
"""

try:
    from gui_main import main
    print("√ gui_main.py 导入成功")
    
    # 测试各个模块的导入
    from gui_components.menu_bar import MenuBar
    print("√ menu_bar.py 导入成功")
    
    from gui_components.toolbar import Toolbar
    print("√ toolbar.py 导入成功")
    
    from gui_components.image_preview import ImagePreview
    print("√ image_preview.py 导入成功")
    
    from gui_components.control_panel import ControlPanel
    print("√ control_panel.py 导入成功")
    
    # 测试控制面板子组件的导入
    from gui_components.control_sections.watermark_type import WatermarkTypeSection
    print("√ watermark_type.py 导入成功")
    
    from gui_components.control_sections.watermark_feature import WatermarkFeatureSection
    print("√ watermark_feature.py 导入成功")
    
    from gui_components.control_sections.operation_scope import OperationScopeSection
    print("√ operation_scope.py 导入成功")
    
    from gui_components.control_sections.text_settings import TextSettingsSection
    print("√ text_settings.py 导入成功")
    
    from gui_components.control_sections.logo_settings import LogoSettingsSection
    print("√ logo_settings.py 导入成功")
    
    from gui_components.control_sections.position import PositionSection
    print("√ position.py 导入成功")
    
    from gui_components.control_sections.opacity import OpacitySection
    print("√ opacity.py 导入成功")
    
    from gui_components.control_sections.rotation import RotationSection
    print("√ rotation.py 导入成功")
    
    from gui_components.control_sections.flip import FlipSection
    print("√ flip.py 导入成功")
    
    from gui_components.control_sections.smart_placement import SmartPlacementSection
    print("√ smart_placement.py 导入成功")
    
    print("\n所有模块导入成功！重构完成。")
    print("\n重构总结：")
    print("- gui_main.py: 主程序入口，包含WatermarkGUI类")
    print("- gui_components/menu_bar.py: 菜单栏组件")
    print("- gui_components/toolbar.py: 工具栏组件")
    print("- gui_components/image_preview.py: 图片预览组件")
    print("- gui_components/control_panel.py: 控制面板主组件")
    print("- gui_components/control_sections/: 控制面板各功能子组件")
    print("  - watermark_type.py: 水印类型选择")
    print("  - watermark_feature.py: 水印功能选择")
    print("  - operation_scope.py: 操作范围选择")
    print("  - text_settings.py: 文字水印设置")
    print("  - logo_settings.py: Logo水印设置")
    print("  - position.py: 水印位置设置")
    print("  - opacity.py: 透明度设置")
    print("  - rotation.py: 旋转角度设置")
    print("  - flip.py: 翻转设置")
    print("  - smart_placement.py: 智能放置")
    
    print("\n重构优势：")
    print("1. 模块化设计，便于维护和扩展")
    print("2. 每个组件职责单一，代码清晰")
    print("3. 易于测试和调试")
    print("4. 支持团队协作开发")
    
    print("\n运行方式：")
    print("python gui_main.py")
    
except ImportError as e:
    print(f"导入失败: {e}")
    print("请检查文件路径和导入语句")
except Exception as e:
    print(f"测试失败: {e}")