"""麦克纳姆轮小车工具管理器.

负责小车工具的初始化、配置和MCP工具注册
"""

from typing import Any, Dict
import sys
import os

# 确保能导入Car_base_control
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.utils.logging_config import get_logger

from .Car_base_control import (
    Car_Forword, Car_back, Car_left, Car_right,
    Car_left_translation, Car_right_translation,
    Car_servo_nod, Car_servo_sayno,
    Car_RGB_Control, Close_RGB,
    Car_Reset, take_photo_agent
)

logger = get_logger(__name__)


class MclumkRobotManager:
    """
    麦克纳姆轮小车工具管理器.
    """

    def __init__(self):
        """
        初始化麦克纳姆轮小车工具管理器.
        """
        self._initialized = False
        logger.info("[MclumkRobotManager] 麦克纳姆轮小车工具管理器初始化")

    def init_tools(self, add_tool, PropertyList, Property, PropertyType):
        """
        初始化并注册所有小车工具.
        """
        try:
            logger.info("[MclumkRobotManager] 开始注册麦克纳姆轮小车工具")

            # 注册前进工具
            self._register_forward_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册后退工具
            self._register_backward_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册左转工具
            self._register_left_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册右转工具
            self._register_right_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册左平移工具
            self._register_left_translation_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册右平移工具
            self._register_right_translation_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册点头工具
            self._register_nod_tool(add_tool, PropertyList)

            # 注册摇头工具
            self._register_sayno_tool(add_tool, PropertyList)

            # 注册RGB灯控制工具
            self._register_rgb_control_tool(add_tool, PropertyList, Property, PropertyType)

            # 注册关闭RGB灯工具
            self._register_close_rgb_tool(add_tool, PropertyList)

            # 注册小车复位工具
            self._register_reset_tool(add_tool, PropertyList)

            # 注册拍照工具
            self._register_take_photo_tool(add_tool, PropertyList)

            self._initialized = True
            logger.info("[MclumkRobotManager] 麦克纳姆轮小车工具注册完成")

        except Exception as e:
            logger.error(f"[MclumkRobotManager] 小车工具注册失败: {e}", exc_info=True)
            raise

    def _register_forward_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册前进工具.
        """

        def forward_wrapper(args: Dict[str, Any]) -> str:
            speed = args.get("speed", 40)
            mytime = args.get("time", 1)
            Car_Forword(speed, mytime)
            return f"小车已前进 {mytime} 秒，速度: {speed}"

        forward_props = PropertyList([
            Property("speed", PropertyType.INTEGER, default_value=40, min_value=0, max_value=100),
            Property("time", PropertyType.INTEGER, default_value=1, min_value=1, max_value=10)
        ])

        add_tool(
            (
                "mclumk_robot.forward",
                "控制小车前进。可以指定速度(0-100)和时间(1-10秒)。",
                forward_props,
                forward_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册前进工具成功")

    def _register_backward_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册后退工具.
        """

        def backward_wrapper(args: Dict[str, Any]) -> str:
            speed = args.get("speed", 40)
            mytime = args.get("time", 1)
            Car_back(speed, mytime)
            return f"小车已后退 {mytime} 秒，速度: {speed}"

        backward_props = PropertyList([
            Property("speed", PropertyType.INTEGER, default_value=40, min_value=0, max_value=100),
            Property("time", PropertyType.INTEGER, default_value=1, min_value=1, max_value=10)
        ])

        add_tool(
            (
                "mclumk_robot.backward",
                "控制小车后退。可以指定速度(0-100)和时间(1-10秒)。",
                backward_props,
                backward_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册后退工具成功")

    def _register_left_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册原地左转工具.
        """

        def left_wrapper(args: Dict[str, Any]) -> str:
            speed = args.get("speed", 50)
            mytime = args.get("time", 1)
            Car_left(speed, mytime)
            return f"小车已原地左转 {mytime} 秒，速度: {speed}"

        left_props = PropertyList([
            Property("speed", PropertyType.INTEGER, default_value=50, min_value=0, max_value=100),
            Property("time", PropertyType.INTEGER, default_value=1, min_value=1, max_value=10)
        ])

        add_tool(
            (
                "mclumk_robot.left",
                "控制小车原地左转。可以指定速度(0-100)和时间(1-10秒)。",
                left_props,
                left_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册原地左转工具成功")

    def _register_right_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册原地右转工具.
        """

        def right_wrapper(args: Dict[str, Any]) -> str:
            speed = args.get("speed", 50)
            mytime = args.get("time", 1)
            Car_right(speed, mytime)
            return f"小车已原地右转 {mytime} 秒，速度: {speed}"

        right_props = PropertyList([
            Property("speed", PropertyType.INTEGER, default_value=50, min_value=0, max_value=100),
            Property("time", PropertyType.INTEGER, default_value=1, min_value=1, max_value=10)
        ])

        add_tool(
            (
                "mclumk_robot.right",
                "控制小车原地右转。可以指定速度(0-100)和时间(1-10秒)。",
                right_props,
                right_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册原地右转工具成功")

    def _register_left_translation_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册左平移工具.
        """

        def left_translation_wrapper(args: Dict[str, Any]) -> str:
            speed = args.get("speed", 45)
            mytime = args.get("time", 1)
            Car_left_translation(speed, mytime)
            return f"小车已左平移 {mytime} 秒，速度: {speed}"

        left_translation_props = PropertyList([
            Property("speed", PropertyType.INTEGER, default_value=45, min_value=0, max_value=100),
            Property("time", PropertyType.INTEGER, default_value=1, min_value=1, max_value=10)
        ])

        add_tool(
            (
                "mclumk_robot.left_translation",
                "控制小车左平移。可以指定速度(0-100)和时间(1-10秒)。",
                left_translation_props,
                left_translation_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册左平移工具成功")

    def _register_right_translation_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册右平移工具.
        """

        def right_translation_wrapper(args: Dict[str, Any]) -> str:
            speed = args.get("speed", 45)
            mytime = args.get("time", 1)
            Car_right_translation(speed, mytime)
            return f"小车已右平移 {mytime} 秒，速度: {speed}"

        right_translation_props = PropertyList([
            Property("speed", PropertyType.INTEGER, default_value=45, min_value=0, max_value=100),
            Property("time", PropertyType.INTEGER, default_value=1, min_value=1, max_value=10)
        ])

        add_tool(
            (
                "mclumk_robot.right_translation",
                "控制小车右平移。可以指定速度(0-100)和时间(1-10秒)。",
                right_translation_props,
                right_translation_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册右平移工具成功")

    def _register_nod_tool(self, add_tool, PropertyList):
        """
        注册点头工具.
        """

        def nod_wrapper(args: Dict[str, Any]) -> str:
            Car_servo_nod()
            return "小车已点头"

        add_tool(
            (
                "mclumk_robot.nod",
                "控制小车点头动作。",
                PropertyList(),
                nod_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册点头工具成功")

    def _register_sayno_tool(self, add_tool, PropertyList):
        """
        注册摇头工具.
        """

        def sayno_wrapper(args: Dict[str, Any]) -> str:
            Car_servo_sayno()
            return "小车已摇头"

        add_tool(
            (
                "mclumk_robot.sayno",
                "控制小车摇头动作。",
                PropertyList(),
                sayno_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册摇头工具成功")

    def _register_rgb_control_tool(self, add_tool, PropertyList, Property, PropertyType):
        """
        注册RGB灯控制工具.
        """

        def rgb_control_wrapper(args: Dict[str, Any]) -> str:
            r = args.get("r", 0)
            g = args.get("g", 0)
            b = args.get("b", 0)
            Car_RGB_Control(r, g, b)
            return f"小车RGB灯已设置为 R:{r}, G:{g}, B:{b}"

        rgb_props = PropertyList([
            Property("r", PropertyType.INTEGER, default_value=0, min_value=0, max_value=255),
            Property("g", PropertyType.INTEGER, default_value=0, min_value=0, max_value=255),
            Property("b", PropertyType.INTEGER, default_value=0, min_value=0, max_value=255)
        ])

        add_tool(
            (
                "mclumk_robot.rgb_control",
                "控制小车RGB灯颜色。可以指定R、G、B值(0-255)。",
                rgb_props,
                rgb_control_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册RGB灯控制工具成功")

    def _register_close_rgb_tool(self, add_tool, PropertyList):
        """
        注册关闭RGB灯工具.
        """

        def close_rgb_wrapper(args: Dict[str, Any]) -> str:
            Close_RGB()
            return "小车RGB灯已关闭"

        add_tool(
            (
                "mclumk_robot.close_rgb",
                "关闭小车RGB灯。",
                PropertyList(),
                close_rgb_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册关闭RGB灯工具成功")

    def _register_reset_tool(self, add_tool, PropertyList):
        """
        注册小车复位工具.
        """

        def reset_wrapper(args: Dict[str, Any]) -> str:
            Car_Reset()
            return "小车已复位"

        add_tool(
            (
                "mclumk_robot.reset",
                "将小车恢复到初始状态，包括关闭RGB灯、重置舵机、停止运动。",
                PropertyList(),
                reset_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册小车复位工具成功")

    def _register_take_photo_tool(self, add_tool, PropertyList):
        """
        注册拍照工具.
        """

        def take_photo_wrapper(args: Dict[str, Any]) -> str:
            take_photo_agent()
            return "小车已拍照"

        add_tool(
            (
                "mclumk_robot.take_photo",
                "控制小车摄像头拍照。",
                PropertyList(),
                take_photo_wrapper,
            )
        )
        logger.debug("[MclumkRobotManager] 注册拍照工具成功")

    def is_initialized(self) -> bool:
        """
        检查管理器是否已初始化.
        """
        return self._initialized


# 全局管理器实例
_mclumk_robot_manager = None


def get_mclumk_robot_manager() -> MclumkRobotManager:
    """
    获取麦克纳姆轮小车工具管理器单例.
    """
    global _mclumk_robot_manager
    if _mclumk_robot_manager is None:
        _mclumk_robot_manager = MclumkRobotManager()
        logger.debug("[MclumkRobotManager] 创建麦克纳姆轮小车工具管理器实例")
    return _mclumk_robot_manager