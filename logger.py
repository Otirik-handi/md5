"""
    ## 日志模块
    默认日志等级为INFO
    
    Update at 2023/06/01
    
    解决了在没有coloredlogs第三方模块的情况logger模块无法使用的问题
"""
import sys
import logging

fmt = '[%(name)s] %(asctime)s [%(levelname)s] [%(filename)s %(funcName)s@lineno:%(lineno)-d] - %(message)s'
logging.basicConfig()
logger = logging.getLogger(name="Logger")

try:
    import coloredlogs
    coloredlogs.install(logger=logger)
    logger.propagate = False
    formatter = coloredlogs.ColoredFormatter(
        fmt=fmt,
        level_styles=dict(
            debug=dict(color='white'),
            info=dict(color='green'),
            warning=dict(color='yellow', bright=True),
            error=dict(color='red', bold=True, bright=True),
            critical=dict(color='black', bold=True, background='red'),
        ),
        field_styles=dict(name=dict(color='white'),
                          asctime=dict(color='white'),
                          lineno=dict(color='white'),
                          funcName=dict(color='blue'),
                          filename=dict(color="white")))

except ModuleNotFoundError:
    formatter = logging.Formatter(fmt=fmt)

sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)
logger.setLevel(logging.INFO)