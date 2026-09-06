import pytest
from qimen4py import calculate, canonical
INPUT={'year':2026,'month':4,'day':10,'hour':14,'minute':30,'timezone':'Asia/Shanghai'}
def test_smoke():
    result=calculate(INPUT)
    assert len(result['palaces'])==9
    assert result['algorithmVersion']=='qimen-zhuanpan-chaibu-v1'
    assert result['juNumber']==1
    assert result['zhiShi']=={'gate':'休门','palace':8}
    assert len(canonical(INPUT)['九宫盘'])==9
def test_late_zi(): assert calculate({'year':2026,'month':4,'day':10,'hour':23,'minute':30,'timezone':'Asia/Shanghai'})['siZhu']==calculate({'year':2026,'month':4,'day':11,'hour':0,'minute':30,'timezone':'Asia/Shanghai'})['siZhu']
def test_invalid_date():
    with pytest.raises(RuntimeError,match='日期无效'): calculate({'year':2026,'month':2,'day':30,'hour':12})
