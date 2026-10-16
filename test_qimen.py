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
    with pytest.raises(ValueError,match='日期无效'): calculate({'year':2026,'month':2,'day':30,'hour':12})

def test_yin_chart():
    result=calculate({'year':2026,'month':9,'day':4,'hour':14,'minute':0,'timezone':'Asia/Shanghai'})
    assert result['dunType']=='yin' and result['juNumber']==1
    assert result['zhiFu']=={'star':'天柱星','palace':2}
    assert result['zhiShi']=={'gate':'惊门','palace':6}
    assert [p['earthStem'] for p in result['palaces']]==list('戊乙丙丁癸壬辛庚己')
