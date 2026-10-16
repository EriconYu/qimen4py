from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from lunar_python import Solar

GAN = list("甲乙丙丁戊己庚辛壬癸")
ZHI = list("子丑寅卯辰巳午未申酉戌亥")
JIA_ZI = [GAN[i % 10] + ZHI[i % 12] for i in range(60)]
TERMS = ["小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"]
PALACES = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]
DIRECTIONS = ["正北", "西南", "正东", "东南", "中央", "西北", "正西", "东北", "正南"]
PALACE_ELEMENTS = ["水", "土", "木", "木", "土", "金", "金", "土", "火"]
EARTH_ORDER = list("戊己庚辛壬癸丁丙乙")
CIRCLE = [3, 8, 1, 6, 5, 0, 7, 2]
STARS = ["天蓬星", "天芮星", "天冲星", "天辅星", "天禽星", "天心星", "天柱星", "天任星", "天英星"]
DOORS = ["休门", "死门", "伤门", "杜门", "", "开门", "惊门", "生门", "景门"]
DEITIES = ["值符", "螣蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天"]
GAN_ELEMENT = dict(zip(GAN, ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]))
STAR_ELEMENT = dict(zip(STARS, ["水", "土", "木", "木", "土", "金", "金", "土", "火"]))
DOOR_ELEMENT = {"休门": "水", "死门": "土", "伤门": "木", "杜门": "木", "开门": "金", "惊门": "金", "生门": "土", "景门": "火"}
BRANCH_PALACE = {"子": 0, "丑": 7, "寅": 7, "卯": 2, "辰": 3, "巳": 3, "午": 8, "未": 1, "申": 1, "酉": 6, "戌": 5, "亥": 5}
RU_MU = {"甲": "未", "乙": "未", "丙": "戌", "丁": "戌", "戊": "戌", "庚": "丑", "辛": "丑", "壬": "辰", "癸": "辰"}
YI_MA = {"申": "寅", "子": "寅", "辰": "寅", "寅": "申", "午": "申", "戌": "申", "亥": "巳", "卯": "巳", "未": "巳", "巳": "亥", "酉": "亥", "丑": "亥"}
SEASONS = {"春": {"木": "旺", "火": "相", "水": "休", "金": "囚", "土": "死"}, "夏": {"火": "旺", "土": "相", "木": "休", "水": "囚", "金": "死"}, "四季土": {"土": "旺", "金": "相", "火": "休", "木": "囚", "水": "死"}, "秋": {"金": "旺", "水": "相", "土": "休", "火": "囚", "木": "死"}, "冬": {"水": "旺", "木": "相", "金": "休", "土": "囚", "火": "死"}}
FORMATIONS = {"乙+丙": "奇仪相佐", "乙+丁": "奇仪相佐", "丙+丁": "星月相会", "丙+戊": "飞鸟跌穴", "丁+戊": "青龙返首", "乙+戊": "日出扶桑", "丙+己": "天遁", "丁+壬": "地遁", "丁+己": "人遁", "丙+壬": "神遁", "乙+癸": "鬼遁", "庚+乙": "太白入荧", "庚+丙": "太白入荧", "庚+丁": "太白入荧", "辛+乙": "白虎猖狂", "乙+辛": "龙逃走", "癸+丁": "腾蛇夭矫", "癸+丙": "蛇矫入火", "庚+戊": "值符飞宫", "庚+壬": "上格", "庚+癸": "大格", "丁+癸": "玉女守门", "戊+壬": "小格", "戊+癸": "刑格", "己+庚": "刑格入狱", "辛+壬": "凶蛇入刑"}


def _rotate(values: list[Any], offset: int) -> list[Any]:
    offset %= len(values)
    return values[offset:] + values[:offset]


def _validate(data: dict[str, Any]) -> None:
    try:
        values = [data[k] for k in ("year", "month", "day", "hour")] + [data.get("minute", 0)]
    except KeyError as exc:
        raise ValueError(f"缺少参数: {exc.args[0]}") from exc
    if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
        raise ValueError("日期和时间必须是整数")
    year, month, day, hour, minute = values
    if not 1900 <= year <= 2100:
        raise ValueError("year 必须在 1900 到 2100 之间")
    if not 1 <= month <= 12:
        raise ValueError("month 必须在 1 到 12 之间")
    if not 0 <= hour <= 23:
        raise ValueError("hour 必须在 0 到 23 之间")
    if not 0 <= minute <= 59:
        raise ValueError("minute 必须在 0 到 59 之间")
    try:
        datetime(year, month, day, hour, minute)
    except ValueError as exc:
        raise ValueError("日期无效") from exc
    if data.get("panType", "zhuan") != "zhuan":
        raise ValueError("目前仅支持转盘奇门")
    if data.get("juMethod", "chaibu") not in ("chaibu", "maoshan"):
        raise ValueError("juMethod 无效")
    if data.get("zhiFuJiGong", "ji_liuyi") not in ("ji_liuyi", "ji_wugong"):
        raise ValueError("zhiFuJiGong 无效")


def _season(branch: str) -> str:
    if branch in "寅卯": return "春"
    if branch in "巳午": return "夏"
    if branch in "辰戌丑未": return "四季土"
    if branch in "申酉": return "秋"
    return "冬"


def _kong(pillar: str) -> tuple[list[str], list[int]]:
    index = JIA_ZI.index(pillar)
    start = (index // 10 * 10) % 60
    used = {JIA_ZI[i][1] for i in range(start, start + 10)}
    branches = [branch for branch in ZHI if branch not in used]
    return branches, [BRANCH_PALACE[branch] + 1 for branch in branches]


def calculate(input_data: dict[str, Any]) -> dict[str, Any]:
    _validate(input_data)
    year, month, day, hour = (input_data[key] for key in ("year", "month", "day", "hour"))
    minute = input_data.get("minute", 0)
    original = datetime(year, month, day, hour, minute)
    effective = original + timedelta(hours=1) if hour == 23 else original
    lunar = Solar.fromYmdHms(effective.year, effective.month, effective.day, effective.hour, effective.minute, 0).getLunar()
    original_lunar = Solar.fromYmd(year, month, day).getLunar()
    pillars = [lunar.getYearInGanZhiExact(), lunar.getMonthInGanZhiExact(), lunar.getDayInGanZhiExact(), lunar.getTimeInGanZhi()]
    term = lunar.getPrevJieQi(False)
    next_term = lunar.getNextJieQi(False)
    term_name = term.getName()
    rotate = (TERMS.index(term_name) - 5) % 24
    element = (JIA_ZI.index(pillars[2]) // 5) % 3
    if input_data.get("juMethod", "chaibu") == "maoshan":
        start = datetime.strptime(term.getSolar().toYmdHms(), "%Y-%m-%d %H:%M:%S")
        element = min(2, int((effective - start).total_seconds() // 432000))
    round_index = int(rotate / 3 + 2) % 8
    direction = 1 if round_index < 4 else -1
    round_number = ([1, 8, 3, 4, 9, 2, 7, 6][round_index] + direction * (rotate % 3) + direction * 6 * element + 17) % 9
    round_number = (round_number + 1) * direction

    earth = [""] * 9
    palace_order = list(range(9))
    start_index = round_number - 1
    if round_number < 0:
        start_index += 1
        palace_order.reverse()
    for palace, stem in zip(_rotate(palace_order, start_index), EARTH_ORDER):
        earth[palace] = stem

    hour_index = JIA_ZI.index(pillars[3])
    conceal = EARTH_ORDER[hour_index // 10]
    conceal_palace = earth.index(conceal)
    middle_palace = 1 if input_data.get("zhiFuJiGong") == "ji_wugong" else (7 if round_number > 0 else 1)
    symbol_index = conceal_palace
    mandate_index = middle_palace if conceal_palace == 4 else conceal_palace

    hour_origin = conceal if pillars[3][0] == "甲" else pillars[3][0]
    offset = (CIRCLE.index(conceal_palace) - CIRCLE.index(earth.index(hour_origin))) % 8
    stars, heaven = [""] * 9, [""] * 9
    star_data = [(palace, earth[palace]) for palace in CIRCLE]
    for palace, (origin, stem) in zip(CIRCLE, _rotate(star_data, offset)):
        stars[palace], heaven[palace] = STARS[origin], stem

    branch_index = ZHI.index(pillars[3][1])
    lead_branch = ZHI.index(JIA_ZI[(hour_index // 10) * 10][1])
    time_offset = (branch_index - lead_branch) % 12
    door_target = (conceal_palace + time_offset * (1 if round_number > 0 else -1)) % 9
    door_target_ring = CIRCLE.index(middle_palace if door_target == 4 else door_target)
    door_offset = CIRCLE.index(mandate_index) - door_target_ring
    doors = [""] * 9
    for palace, door_origin in zip(CIRCLE, _rotate(CIRCLE, door_offset)):
        doors[palace] = DOORS[door_origin]

    symbol_name = STARS[symbol_index]
    symbol_palace = stars.index(symbol_name)
    deity_order = DEITIES if round_number > 0 else list(reversed(DEITIES))
    deity_offset = (CIRCLE.index(symbol_palace) - deity_order.index("值符")) % 8
    deities = [""] * 9
    for palace, deity in zip(CIRCLE, _rotate(deity_order, -deity_offset)):
        deities[palace] = deity

    season = _season(pillars[1][1])
    day_kong, day_kong_palaces = _kong(pillars[2])
    hour_kong, hour_kong_palaces = _kong(pillars[3])
    yi_ma_branch = YI_MA[pillars[2][1]]
    yi_ma_palace = BRANCH_PALACE[yi_ma_branch]
    palaces, global_formations = [], []
    opposites = {0: 8, 8: 0, 1: 7, 7: 1, 2: 6, 6: 2, 3: 5, 5: 3}
    for index in range(9):
        formations: list[str] = []
        key = f"{heaven[index]}+{earth[index]}"
        if index != 4 and key in FORMATIONS:
            formations.append(FORMATIONS[key])
        if stars[index] and STARS.index(stars[index]) == index:
            formations.append("伏吟")
        if stars[index] and opposites.get(STARS.index(stars[index])) == index:
            formations.append("反吟")
        global_formations.extend(f"{PALACES[index]}宫: {formation}" for formation in formations)
        mu_palace = BRANCH_PALACE.get(RU_MU.get(heaven[index], ""), -1)
        palaces.append({"palaceIndex": index + 1, "palaceName": PALACES[index], "direction": DIRECTIONS[index], "element": PALACE_ELEMENTS[index], "earthStem": earth[index], "earthStemElement": GAN_ELEMENT.get(earth[index], ""), "heavenStem": heaven[index], "heavenStemElement": GAN_ELEMENT.get(heaven[index], ""), "star": stars[index], "starElement": STAR_ELEMENT.get(stars[index], ""), "gate": doors[index], "gateElement": DOOR_ELEMENT.get(doors[index], ""), "deity": deities[index], "formations": formations, "stemWangShuai": SEASONS[season].get(GAN_ELEMENT.get(heaven[index], ""), ""), "elementState": SEASONS[season][PALACE_ELEMENTS[index]], "isKongWang": index + 1 in day_kong_palaces or index + 1 in hour_kong_palaces, "isYiMa": index == yi_ma_palace, "isRuMu": index == mu_palace})

    term_start = term.getSolar().toYmdHms()[:16]
    term_end = next_term.getSolar().toYmdHms()[:16]
    return {"algorithmVersion": "qimen-zhuanpan-chaibu-v1", "dateInfo": {"solarDate": f"{year:04d}-{month:02d}-{day:02d}", "lunarDate": f"{original_lunar.getYearInChinese()}年{original_lunar.getMonthInChinese()}月{original_lunar.getDayInChinese()}", "solarTerm": term_name, "solarTermRange": f"{term_start} ~ {term_end}"}, "siZhu": dict(zip(("year", "month", "day", "hour"), pillars)), "dunType": "yang" if round_number > 0 else "yin", "juNumber": abs(round_number), "yuan": ["上元", "中元", "下元"][element], "xunShou": "甲" + JIA_ZI[(hour_index // 10) * 10][1], "zhiFu": {"star": symbol_name, "palace": symbol_palace + 1}, "zhiShi": {"gate": DOORS[mandate_index], "palace": doors.index(DOORS[mandate_index]) + 1}, "palaces": palaces, "kongWang": {"dayKong": {"branches": day_kong, "palaces": day_kong_palaces}, "hourKong": {"branches": hour_kong, "palaces": hour_kong_palaces}}, "yiMa": {"branch": yi_ma_branch, "palace": yi_ma_palace + 1}, "globalFormations": global_formations, "panType": "转盘", "juMethod": "茅山法" if input_data.get("juMethod") == "maoshan" else "拆补法", **({"question": input_data["question"]} if "question" in input_data else {}), "monthPhase": {stem: SEASONS[season][GAN_ELEMENT[stem]] for stem in GAN}}


def canonical(input_data: dict[str, Any]) -> dict[str, Any]:
    result = calculate(input_data)
    basic = {"四柱": " ".join(result["siZhu"].values()), "节气": result["dateInfo"]["solarTerm"], "局式": ("阳遁" if result["dunType"] == "yang" else "阴遁") + str(result["juNumber"]) + "局", "三元": result["yuan"], "旬首": result["xunShou"], "值符": result["zhiFu"]["star"], "值使": result["zhiShi"]["gate"]}
    if "question" in result: basic["占问"] = result["question"]
    day_kong = set(result["kongWang"]["dayKong"]["palaces"])
    hour_kong = set(result["kongWang"]["hourKong"]["palaces"])
    board = []
    for palace in result["palaces"]:
        status = [label for condition, label in ((palace["palaceIndex"] in day_kong, "日空"), (palace["palaceIndex"] in hour_kong, "时空"), (palace["isYiMa"], "驿马"), (palace["isRuMu"], "入墓")) if condition]
        if palace["palaceIndex"] == 5: status = ["寄宫参看对应宫位"]
        item = {"宫名": palace["palaceName"], "宫位序号": palace["palaceIndex"], "宫位": palace["palaceName"] + str(palace["palaceIndex"]), "宫位五行": palace["element"] or "-", "八神": palace["deity"] or "-", "九星": palace["star"] or "-"}
        if palace["starElement"]: item["九星五行"] = palace["starElement"]
        item["八门"] = palace["gate"] or "-"
        if palace["gateElement"]: item["八门五行"] = palace["gateElement"]
        item.update({"天盘天干": palace["heavenStem"] or "-", "地盘天干": palace["earthStem"] or "-", "宫位状态": status})
        board.append(item)
    return {"基本信息": basic, "九宫盘": board}


__all__ = ["calculate", "canonical"]
