from qimen4py import calculate
INPUT={'year':2026,'month':4,'day':10,'hour':14,'minute':30,'timezone':'Asia/Shanghai'}
def test_smoke(): assert len(calculate(INPUT)['palaces'])==9
def test_late_zi(): assert calculate({'year':2026,'month':4,'day':10,'hour':23,'minute':30,'timezone':'Asia/Shanghai'})['siZhu']==calculate({'year':2026,'month':4,'day':11,'hour':0,'minute':30,'timezone':'Asia/Shanghai'})['siZhu']
