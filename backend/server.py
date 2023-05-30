from Wrapper import WrapperDB

wp = WrapperDB()

wp.addLog(('2023-05-30 22:10:32', 'il mio bellissimo motivo', 3))
print(wp.deleteLog(5))
# wp.modifyLog(4, ('2023-05-30 22:11:32', 'il mio bellissimo motivo', 3))
print(wp.getLog())
