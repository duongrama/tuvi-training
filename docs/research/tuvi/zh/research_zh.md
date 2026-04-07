# 紫微斗数 (Zi Wei Dou Shu) Research — Chinese Sources

**Research date:** 2026-03-16
**Purpose:** Technical reference for Vietnamese Tu Vi implementation — original Chinese system

---

## Table of Contents

1. [Overview and Schools](#1-overview-and-schools)
2. [The 12 Palaces (十二宫)](#2-the-12-palaces-十二宫)
3. [Five Element Bureau (五行局)](#3-five-element-bureau-五行局)
4. [Complete Star Catalog (108 Stars)](#4-complete-star-catalog-108-stars)
5. [Star Placement Rules (安星诀)](#5-star-placement-rules-安星诀)
6. [庙旺平陷 System (Star Dignity/Brightness)](#6-庙旺平陷-system)
7. [四化 System (Tứ Hóa / Four Transformations)](#7-四化-system)
8. [命主 and 身主 (Life/Body Masters)](#8-命主-and-身主)
9. [Palace Heavenly Stems (宫干)](#9-palace-heavenly-stems-宫干)
10. [大限, 小限, 流年 (Major/Minor Cycles)](#10-大限-小限-流年)
11. [飞化 (Flying Transformations)](#11-飞化-flying-transformations)
12. [Scoring Systems](#12-scoring-systems)
13. [Reference Apps and Tools](#13-reference-apps-and-tools)

---

## 1. Overview and Schools

紫微斗数 (Zi Wei Dou Shu, lit. "Purple Star Astrology") is a Chinese astrology system attributed to 陈希夷 (Chen Xiyi, Song Dynasty). The Vietnamese system 紫微/Tử Vi is derived directly from it.

### Major Schools (派别)

- **南派 (Southern School)**: More traditional, focuses on star combinations and dignity levels
- **北派 (Northern School)**: Emphasizes transformations (四化)
- **飞星派 (Flying Star School)**: Advanced technique using palace heavenly stems to generate additional 四化 layers

---

## 2. The 12 Palaces (十二宫)

The 12 palaces are fixed by birth date/time. Each palace governs a life domain:

| Palace | Chinese | Vietnamese | Domain |
|--------|---------|-----------|--------|
| 命宫 | 命宫 | Mệnh | Core self, destiny |
| 兄弟宫 | 兄弟宫 | Huynh Đệ | Siblings, colleagues |
| 夫妻宫 | 夫妻宫 | Phu Thê | Marriage, partners |
| 子女宫 | 子女宫 | Tử Tức | Children |
| 财帛宫 | 财帛宫 | Tài Bạch | Wealth |
| 疾厄宫 | 疾厄宫 | Tật Ách | Health |
| 迁移宫 | 迁移宫 | Thiên Di | Travel, social |
| 仆役宫 | 仆役宫 | Nô Bộc | Subordinates |
| 官禄宫 | 官禄宫 | Quan Lộc | Career |
| 田宅宫 | 田宅宫 | Điền Trạch | Property, home |
| 福德宫 | 福德宫 | Phúc Đức | Spiritual fortune |
| 父母宫 | 父母宫 | Phụ Mẫu | Parents |

**Palace earthly branch assignment** is determined by birth month and hour (see step 1 of chart construction).

---

## 3. Five Element Bureau (五行局)

The Five Element Bureau (命宫纳音五行局) determines the starting age for 大限 and the placement anchor for 紫微星. It is calculated from the 纳音 (Nayin) of the 命宫's heavenly stem and earthly branch combination.

| Bureau | Chinese | Vietnamese | 大限 Start Age | 紫微 Starting Palace |
|--------|---------|-----------|--------------|---------------------|
| 水二局 | Water 2 | Thủy Nhị Cục | Age 2 | 申 palace |
| 木三局 | Wood 3 | Mộc Tam Cục | Age 3 | 亥 palace |
| 金四局 | Metal 4 | Kim Tứ Cục | Age 4 | 巳 palace |
| 土五局 | Earth 5 | Thổ Ngũ Cục | Age 5 | 申 palace |
| 火六局 | Fire 6 | Hỏa Lục Cục | Age 6 | 寅 palace |

**Calculation formula:**
- Stem value: 甲乙=1, 丙丁=2, 戊己=3, 庚辛=4, 壬癸=5
- Branch value: 子午丑未=1, 寅申卯酉=2, 辰戌巳亥=3
- Sum = bureau number (subtract 5 if > 5)
  - 1=水二局, 2=木三局, 3=金四局, 4=土五局, 5=火六局

---

## 4. Complete Star Catalog (108 Stars)

### 4.1 甲级星 (Grade A — 28 Stars, Most Important)

#### 十四主星 (14 Main Stars)

| # | Chinese | Vietnamese | Element | System |
|---|---------|-----------|---------|--------|
| 1 | 紫微 | Tử Vi | Earth/North | 紫微系 |
| 2 | 天机 | Thiên Cơ | Wood | 紫微系 |
| 3 | 太阳 | Thái Dương | Fire/Sun | 紫微系 |
| 4 | 武曲 | Vũ Khúc | Metal | 紫微系 |
| 5 | 天同 | Thiên Đồng | Water | 紫微系 |
| 6 | 廉贞 | Liêm Trinh | Fire | 紫微系 |
| 7 | 天府 | Thiên Phủ | Earth/South | 天府系 |
| 8 | 太阴 | Thái Âm | Water/Moon | 天府系 |
| 9 | 贪狼 | Tham Lang | Water/Wood | 天府系 |
| 10 | 巨门 | Cự Môn | Water | 天府系 |
| 11 | 天相 | Thiên Tướng | Water | 天府系 |
| 12 | 天梁 | Thiên Lương | Earth | 天府系 |
| 13 | 七杀 | Thất Sát | Metal | 天府系 |
| 14 | 破军 | Phá Quân | Water | 天府系 |

#### 四化星 (4 Transformation Stars — Grade A)

| Chinese | Vietnamese | Meaning |
|---------|-----------|---------|
| 化禄 | Hóa Lộc | Prosperity, opportunity |
| 化权 | Hóa Quyền | Authority, power |
| 化科 | Hóa Khoa | Culture, benefactors |
| 化忌 | Hóa Kỵ | Obstacles, challenges |

#### 六吉星 (6 Auspicious Auxiliary Stars — Grade A)

| Chinese | Vietnamese | Placement Rule |
|---------|-----------|---------------|
| 左辅 | Tả Phụ | From 辰, count forward by birth month |
| 右弼 | Hữu Bật | From 戌, count backward by birth month |
| 文昌 | Văn Xương | From 戌, count backward by birth hour |
| 文曲 | Văn Khúc | From 辰, count forward by birth hour |
| 天魁 | Thiên Khôi | By birth year stem (see table below) |
| 天钺 | Thiên Việt | By birth year stem (see table below) |

**天魁/天钺 by birth year stem:**

| Stem | 天魁 palace | 天钺 palace |
|------|------------|------------|
| 甲/戊/庚 | 丑 | 未 |
| 乙/己 | 子 | 申 |
| 丙/丁 | 亥 | 酉 |
| 辛 | 午 | 寅 |
| 壬/癸 | 卯 | 巳 |

#### 六凶星 (6 Inauspicious Stars — Grade A)

| Chinese | Vietnamese | Placement Rule |
|---------|-----------|---------------|
| 擎羊 | Kình Dương | 1 palace after 禄存 |
| 陀罗 | Đà La | 1 palace before 禄存 |
| 火星 | Hỏa Tinh | By birth year branch + birth hour (forward) |
| 铃星 | Linh Tinh | By birth year branch + birth hour (forward) |
| 地空 | Địa Không | From 亥, count backward by birth hour |
| 地劫 | Địa Kiếp | From 亥, count forward by birth hour |

**禄存 placement (determines 擎羊/陀罗):**

| Stem | 禄存 palace |
|------|-----------|
| 甲 | 寅 |
| 乙 | 卯 |
| 丙/戊 | 巳 |
| 丁/己 | 午 |
| 庚 | 申 |
| 辛 | 酉 |
| 壬 | 亥 |
| 癸 | 子 |

**天马 (Heavenly Horse) placement:**

| Birth year branch | 天马 palace |
|------------------|-----------|
| 寅/午/戌 | 申 |
| 申/子/辰 | 寅 |
| 巳/酉/丑 | 亥 |
| 亥/卯/未 | 巳 |

---

### 4.2 乙级星 (Grade B — 29+ Stars, Refine Character)

These stars refine personality/destiny in detail. Full list:

| Chinese | Vietnamese equiv | Function |
|---------|-----------------|---------|
| 红鸾 | Hồng Loan | Romance, marriage timing |
| 天喜 | Thiên Hỷ | Joy, celebration |
| 天刑 | Thiên Hình | Law, punishment, medical |
| 天姚 | Thiên Diêu | Charm, sensuality |
| 解神 | Giải Thần | Relief from problems |
| 天巫 | Thiên Vu | Spirituality, divination |
| 天月 | Thiên Việt | Health matters |
| 阴煞 | Âm Sát | Hidden threats |
| 天哭 | Thiên Khốc | Grief, sorrow |
| 天虚 | Thiên Hư | Emptiness, loss |
| 龙池 | Long Trì | Talent, culture |
| 凤阁 | Phượng Các | Elegance, beauty |
| 台辅 | Đài Phụ | Status, support |
| 封诰 | Phong Cáo | Official recognition |
| 三台 | Tam Thai | Status improvement |
| 八座 | Bát Tọa | Position, seat |
| 恩光 | Ân Quang | Benefactor's favor |
| 天贵 | Thiên Quý | Noble status |
| 孤辰 | Cô Thần | Solitude (male) |
| 寡宿 | Quả Tú | Solitude (female) |
| 蜚廉 | Phi Liêm | Disputes, slander |
| 破碎 | Phá Toái | Broken things |
| 华盖 | Hoa Cái | Spirituality, isolation |
| 咸池 | Hàm Trì | Desires, sexuality |
| 天德 | Thiên Đức | Virtue, protection |
| 月德 | Nguyệt Đức | Lunar virtue |
| 天才 | Thiên Tài | Intelligence, talent |
| 天寿 | Thiên Thọ | Longevity |
| 劫煞 | Kiếp Sát | Robbery, disaster |

---

### 4.3 丙级星 (Grade C — Three Groups of 12 Rotating Stars)

These are annual/decadal timing stars, placed by age or year. They rotate around the chart.

#### 博士十二神 (12 Doctor Stars — placed by 大限 direction from 禄存)

| # | Chinese | Vietnamese | Nature |
|---|---------|-----------|--------|
| 1 | 博士 | Bác Sĩ | Knowledge, officials |
| 2 | 力士 | Lực Sĩ | Power, violence |
| 3 | 青龙 | Thanh Long | Wealth, success |
| 4 | 小耗 | Tiểu Hao | Minor loss |
| 5 | 将军 | Tướng Quân | Authority, conflict |
| 6 | 奏书 | Tấu Thư | Documents, petitions |
| 7 | 飞廉 | Phi Liêm | Trouble, legal issues |
| 8 | 喜神 | Hỷ Thần | Happiness |
| 9 | 病符 | Bệnh Phù | Illness |
| 10 | 大耗 | Đại Hao | Major loss |
| 11 | 伏兵 | Phục Binh | Hidden enemies |
| 12 | 官符 | Quan Phù | Legal entanglements |

**Placement:** Start from 禄存 palace, count forward (Yang male/Yin female) or backward (Yin male/Yang female) for 大限 age.

#### 长生十二神 (12 Life Cycle Stages — placed by Five Element Bureau)

| # | Chinese | Vietnamese | Meaning |
|---|---------|-----------|---------|
| 1 | 长生 | Trường Sinh | Birth/vitality |
| 2 | 沐浴 | Mộc Dục | Bath — vulnerability |
| 3 | 冠带 | Quan Đới | Coming of age |
| 4 | 临官 | Lâm Quan | Official position |
| 5 | 帝旺 | Đế Vượng | Peak power |
| 6 | 衰 | Suy | Decline |
| 7 | 病 | Bệnh | Illness |
| 8 | 死 | Tử | Death |
| 9 | 墓 | Mộ | Tomb |
| 10 | 绝 | Tuyệt | Extinction |
| 11 | 胎 | Thai | Gestation |
| 12 | 养 | Dưỡng | Nourishment |

**Starting palace by Five Element Bureau:**
- 水二局: 长生 at 申
- 木三局: 长生 at 亥
- 金四局: 长生 at 巳
- 土五局: 长生 at 申
- 火六局: 长生 at 寅

**Direction:** Yang male + Yin female = forward; Yin male + Yang female = reverse.

#### 岁前十二神 / 太岁十二神 (12 Year God Stars — placed by 流年)

| # | Chinese | Vietnamese | Nature |
|---|---------|-----------|--------|
| 1 | 岁建 | Tuế Kiến | Year start, authority |
| 2 | 晦气 | Hối Khí | Gloom, setbacks |
| 3 | 丧门 | Tang Môn | Mourning, death in family |
| 4 | 贯索 | Quán Sách | Imprisonment, restriction |
| 5 | 官符 | Quan Phù | Legal troubles |
| 6 | 小耗 | Tiểu Hao | Minor financial loss |
| 7 | 大耗 | Đại Hao | Major financial loss |
| 8 | 龙德 | Long Đức | Good fortune |
| 9 | 白虎 | Bạch Hổ | Accidents, blood events |
| 10 | 天德 | Thiên Đức | Heavenly virtue |
| 11 | 吊客 | Điếu Khách | Grief, mourning |
| 12 | 病符 | Bệnh Phù | Illness |

**Placement:** 岁建 at the 流年地支 palace, others follow clockwise.

#### 将前十二神 (12 General Stars — placed by 流年)

| # | Chinese | Vietnamese |
|---|---------|-----------|
| 1 | 将星 | Tướng Tinh |
| 2 | 攀鞍 | Ban An |
| 3 | 岁驿 | Tuế Dịch |
| 4 | 息神 | Tức Thần |
| 5 | 华盖 | Hoa Cái |
| 6 | 劫煞 | Kiếp Sát |
| 7 | 灾煞 | Tai Sát |
| 8 | 天煞 | Thiên Sát |
| 9 | 指背 | Chỉ Bối |
| 10 | 咸池 | Hàm Trì |
| 11 | 月煞 | Nguyệt Sát |
| 12 | 亡神 | Vong Thần |

---

### 4.4 丁/戊级星 (Grade D/E — Flow Year Minor Stars)

These appear only in flow year analysis and include:
岁建, 龙德, 天德, 将星, 攀鞍, 岁驿, 华盖, 飞廉, 喜神, and the inauspicious 白虎, 吊客, 病符, 丧门, 贯索 etc.

---

### 4.5 截路空亡 (Path Interruption and Void Pairs)

Based on the **birth year's heavenly stem**, two earthly branch palaces are "voided":

| Birth year stem | 截路 (Jié Lù) | 空亡 (Kōng Wáng) |
|----------------|--------------|-----------------|
| 甲/己 | 申 | 酉 |
| 乙/庚 | 午 | 未 |
| 丙/辛 | 辰 | 巳 |
| 丁/壬 | 寅 | 卯 |
| 戊/癸 | 子 | 丑 |

Stars in these palaces have weakened or blocked effect.

---

## 5. Star Placement Rules (安星诀)

### 5.1 Chart Construction Order

1. Determine 命宫 from birth month + hour
2. Place 12 palace labels (earthly branches) around the chart
3. Calculate 五行局 from 命宫 nayin
4. Place 紫微星 using birth day + bureau number
5. Place remaining 13 main stars from 紫微 and 天府 positions
6. Place all auxiliary stars by their respective rules

### 5.2 紫微星 Placement Algorithm

Mnemonic: "生日除局商为月，一自寅起紫微定。只加不减到整除，阳退阴进记心中。"

Method:
- Divide lunar birth day by bureau number
- Quotient maps to palace (寅=1, 卯=2, 辰=3, 巳=4, 午=5, 未=6, 申=7, 酉=8, 戌=9, 亥=10, 子=11, 丑=12)
- If remainder is odd: move 紫微 backward (counter-clockwise) by remainder steps
- If remainder is even: move 紫微 forward (clockwise) by remainder steps
- If no remainder: 紫微 stays at the quotient palace

### 5.3 14 Main Stars Placement From 紫微

**紫微系 (Zi Wei Group) — counter-clockwise from 紫微:**

Mnemonic: "紫微逆去天机星，隔一太阳武曲辰，连接天同空二宫，廉贞居处方是真。"

Pattern (counter-clockwise): 紫微, [skip], 天机, [skip 1], 太阳, 武曲, 天同, [skip 2], 廉贞

**天府系 (Tian Fu Group) — clockwise from 天府:**

天府 is always in the palace that forms a 命宫-对 mirror with 紫微.
Mnemonic: "天府顺行有太阴，贪狼而后巨门临，随来天相天梁继，七杀空三是破军。"

Pattern (clockwise): 天府, 太阴, 贪狼, 巨门, 天相, 天梁, 七杀, [skip 3], 破军

---

## 6. 庙旺平陷 System

### 6.1 Dignity Levels

There are typically **5 levels** (sometimes expanded to 7):

| Level | Chinese | Vietnamese | Star Condition |
|-------|---------|-----------|---------------|
| 庙 | 庙 | Miếu | Brightest — auspicious stars extremely auspicious, inauspicious stars neutralized |
| 旺 | 旺 | Vượng | Very bright — auspicious stars auspicious, inauspicious stars mild |
| 得 | 得地 | Đắc | Moderately bright — auspicious stars useful, inauspicious stars begin showing |
| 平 | 平 | Bình/Hãm nhẹ | Weak light — auspicious stars have little power, inauspicious stars active |
| 陷 | 陷 | Hãm | No light — auspicious stars powerless, inauspicious stars at maximum harm |

Extended 7-level system: 庙 > 旺 > 得地 > 利益 > 平和 > 不得地 > 陷

### 6.2 Stars Minimally Affected by Dignity

These 5 stars maintain relatively fixed characteristics regardless of dignity:
**紫微, 天府, 七杀, 破军, 武曲**

Their power comes primarily from star combinations and transformations, not brightness level.

### 6.3 Stars Significantly Affected by Dignity

These 9 stars change substantially based on dignity:
**天机, 太阳, 太阴, 天同, 巨门, 贪狼, 天相, 廉贞, 天梁**

### 6.4 Key Dignity Patterns (Partial Table)

| Star | 庙 | 旺 | 平 | 陷 |
|------|----|----|----|----|
| 天机 | 卯, 酉 | 子, 巳 | (others) | 辰, 戌 |
| 太阳 | 寅, 卯, 辰 | 午 | (others) | 酉, 戌, 亥 |
| 太阴 | 子 | 亥, 丑 | (others) | 午, 巳 |
| 天同 | 子, 午 | 卯, 酉 | (others) | 寅, 申 |
| 巨门 | 子, 亥 | 卯, 酉 | (others) | 午, 巳 |
| 廉贞 | 寅, 申 | 午 | (others) | 卯, 酉 |
| 天梁 | 午 | 寅, 申 | (others) | 子 |
| 贪狼 | 寅, 申 | 卯, 酉 | (others) | 辰, 戌 |
| 天相 | 寅, 午, 戌 | 亥, 卯, 未 | (others) | 辰, 巳 |

**Important principle:** "入庙不一定吉，失陷不一定凶" — Temple position doesn't guarantee auspiciousness; fallen position doesn't guarantee inauspiciousness. Always analyze in context with the full chart, combinations, and 四化.

---

## 7. 四化 System

### 7.1 Complete 四化 Table (Ten Heavenly Stems)

| 天干 | 化禄 (Hóa Lộc) | 化权 (Hóa Quyền) | 化科 (Hóa Khoa) | 化忌 (Hóa Kỵ) |
|------|--------------|----------------|--------------|--------------|
| 甲 | 廉贞 | 破军 | 武曲 | 太阳 |
| 乙 | 天机 | 天梁 | 紫微 | 太阴 |
| 丙 | 天同 | 天机 | 文昌 | 廉贞 |
| 丁 | 太阴 | 天同 | 天机 | 巨门 |
| 戊 | 贪狼 | 太阴 | 右弼 | 天机 |
| 己 | 武曲 | 贪狼 | 天梁 | 文曲 |
| 庚 | 太阳 | 武曲 | 太阴 | 天同 |
| 辛 | 巨门 | 太阳 | 文曲 | 文昌 |
| 壬 | 天梁 | 紫微 | 左辅 | 武曲 |
| 癸 | 破军 | 巨门 | 太阴 | 贪狼 |

### 7.2 Meanings

- **化禄 (Hóa Lộc):** Prosperity, smooth sailing, opportunities, financial gain, socializing
- **化权 (Hóa Quyền):** Authority, decisive action, leadership, competitiveness
- **化科 (Hóa Khoa):** Academic success, cultural refinement, benefactor support, good reputation
- **化忌 (Hóa Kỵ):** Obstacles, fixation, loss, challenges; the star's negative qualities are amplified

### 7.3 Layers of 四化

There are multiple simultaneous layers of 四化 operating on a chart:

1. **生年四化 (Birth Year Transformations):** Based on birth year's heavenly stem — permanent, foundational
2. **大限四化 (Major Period Transformations):** Based on the 大限 palace's heavenly stem
3. **流年四化 (Annual Transformations):** Based on the current year's heavenly stem

---

## 8. 命主 and 身主

### 8.1 命主 (Ming Zhu / Life Master Star)

Determined by the **earthly branch of 命宫**:

| 命宫 earthly branch | 命主 star |
|--------------------|----------|
| 子 | 贪狼 (Tham Lang) |
| 丑 / 亥 | 巨门 (Cự Môn) |
| 寅 / 戌 | 禄存 (Lộc Tồn) |
| 卯 / 酉 | 文曲 (Văn Khúc) |
| 巳 / 未 | 武曲 (Vũ Khúc) |
| 辰 / 申 | 廉贞 (Liêm Trinh) |
| 午 | 破军 (Phá Quân) |

命主 governs the **first half of life** and represents innate destiny.

### 8.2 身主 (Shen Zhu / Body Master Star)

Determined by the **earthly branch of birth year**:

| Birth year branch | 身主 star |
|------------------|----------|
| 子 | 火星 (Hỏa Tinh) |
| 午 | 铃星 (Linh Tinh) |
| 丑 / 未 | 天相 (Thiên Tướng) |
| 寅 / 申 | 天梁 (Thiên Lương) |
| 卯 / 酉 | 天同 (Thiên Đồng) |
| 巳 / 亥 | 天机 (Thiên Cơ) |
| 辰 / 戌 | 文昌 (Văn Xương) |

身主 governs the **second half of life** and represents acquired fortune.

### 8.3 身宫 Position

身宫 is determined by birth hour:

| Birth hour (地支) | 身宫 location |
|-----------------|-------------|
| 子 / 午 | Same palace as 命宫 |
| 卯 / 酉 | 迁移宫 |
| 寅 / 申 | 官禄宫 |
| 辰 / 戌 | 财帛宫 |
| 巳 / 亥 | 夫妻宫 |
| 丑 / 未 | 福德宫 |

---

## 9. Palace Heavenly Stems (宫干)

Each of the 12 palaces has an assigned heavenly stem. This is critical for 飞化 (flying transformation) calculations.

**Method — Five Tiger Stem Displacement (五虎遁干):**

Based on the birth year's heavenly stem, find the stem assigned to 寅 palace, then continue clockwise through 12 palaces in the fixed stem sequence (甲乙丙丁戊己庚辛壬癸甲乙...):

| Birth year stem | 寅 palace stem |
|----------------|--------------|
| 甲 / 己 | 丙 |
| 乙 / 庚 | 戊 |
| 丙 / 辛 | 庚 |
| 丁 / 壬 | 壬 |
| 戊 / 癸 | 甲 |

Mnemonic: "甲己之年丙作首，乙庚之岁戊为头，丙辛岁首寻庚起，丁壬壬位顺行流，若言戊癸何方发，甲寅之上好追求"

From 寅's stem, assign stems clockwise: 寅, 卯, 辰, 巳, 午, 未, 申, 酉, 戌, 亥, 子, 丑.

Example: Birth year stem 甲 → 寅=丙, 卯=丁, 辰=戊, 巳=己, 午=庚, 未=辛, 申=壬, 酉=癸, 戌=甲, 亥=乙, 子=丙, 丑=丁

---

## 10. 大限, 小限, 流年 (Major/Minor Cycles)

### 10.1 大限 (Dà Xiàn — 10-Year Major Period)

- Life is divided into 12 major periods of 10 years each
- **Starting age** = Five Element Bureau number (水2=age 2, 木3=age 3, etc.)
- **Direction:** Yang males + Yin females go **forward (clockwise)** from 命宫; Yin males + Yang females go **backward (counter-clockwise)**
- **大限 palace sequence:** Each 大限 occupies one palace for 10 years

**Determining Yang/Yin:**
- Yang male: born in 甲丙戊庚壬 years
- Yin female: born in 甲丙戊庚壬 years
- Yin male: born in 乙丁己辛癸 years
- Yang female: born in 乙丁己辛癸 years

### 10.2 大限 Palace Heavenly Stem

The 大限 palace has its own heavenly stem (from the 宫干 system). This stem generates the **大限四化** — four additional transformation stars overlaid on the natal chart for that 10-year period.

### 10.3 小限 (Xiǎo Xiàn — Annual Minor Period)

- One palace per year, advancing annually
- Males start 小限 at 寅 palace from age 1; females start at 午 or 申 (varies by school)
- Each year the 小限 moves one palace forward/backward

### 10.4 流年 (Liú Nián — Annual Flow Year)

- Determined by the current year's earthly branch
- The 流年命宫 is the palace matching the current year's earthly branch
- **流年四化:** Based on the current year's heavenly stem
- 12 岁前十二神 rotate from 流年命宫

### 10.5 流月 (Monthly) and 流日 (Daily)

- 流月命宫 starts at 寅 palace of the 流年命宫 palace, advancing monthly
- 流日 follows a similar sub-cycle within each month

---

## 11. 飞化 (Flying Transformations — Advanced Technique)

飞化 is an advanced technique primarily used in the **飞星派 (Flying Star School)**. It generates additional layers of 四化 using palace heavenly stems.

### 11.1 How 飞化 Works

Each palace has a heavenly stem (宫干). That stem generates a set of 四化, which "fly into" (affect) other palaces. This creates a web of cause-and-effect between palaces.

- When a 化忌 flies from palace A into palace B, it creates a specific life event connection between the two life domains
- When a 化禄 flies into a palace, it brings prosperity to that domain

### 11.2 自化 (Self-Transformation)

自化 occurs when a palace's own 宫干 generates a 四化 that hits a star already in that same palace. This is considered a "self-contained" transformation — the palace acts on itself.

**Relative power:** 自化 > 飞宫 (flying to another palace). Self-transformation is considered a direct linear force; flying transformation is a parabolic (indirect) force.

### 11.3 化入 vs 化出

- **化入:** 四化 flies INTO 命宫, 官禄宫, 财帛宫, 田宅宫 = external forces affecting core life domains
- **化出:** 四化 flies INTO 兄弟宫, 夫妻宫, 子女宫, 疾厄宫, 迁移宫, 仆役宫, 福德宫, 父母宫 = energy flowing outward to relationship/peripheral domains

### 11.4 Multi-Layer Analysis

Professional analysis uses **三盘 (Three Charts)** simultaneously:
1. **本命盘 (Natal chart)** — weight 5/10, foundational
2. **大限盘 (Major period chart)** — weight 3/10, running fortune
3. **流年盘 (Annual chart)** — weight 2/10, triggering events

---

## 12. Scoring Systems

### 12.1 Chinese Professional Scoring Method

Chinese 紫微斗数 apps and masters use a relative palace strength scoring system:

**Basic scoring principles:**

1. **Main star dignity:** 主星庙旺 = +1 to +2 points; 主星落陷 = -1 to -2 points
2. **Auspicious auxiliary stars present:** 左辅, 右弼, 天魁, 天钺, 文昌, 文曲 = +1 each
3. **Inauspicious stars present:** 擎羊, 陀罗, 火星, 铃星, 地空, 地劫, 化忌 = -1 each
4. **三方四正 (Three Directions + Opposite palace):** Stars in these 4 related palaces also count
5. **Positive 四化 present:** 化禄, 化权, 化科 = +1 each
6. **化忌 present:** -2 points (heavier penalty)

**Result:** Sum scores for each palace → rank palaces from strongest to weakest. Strongest = that person's advantage domain; weakest = that person's life challenge area.

### 12.2 Software Examples

- **道显紫微排盘软件 v14:** Advanced 四化分象 analysis, chart reverse-engineering
- **陈剑紫微软件 v5.0:** 150 deduction rules, auspicious/inauspicious pattern recognition
- **神机阁 (shenjige.cn):** Online chart + palace-by-palace interpretation
- **星尘算命 (kvov.com):** Free online chart with star explanations

---

## 13. Reference Apps and Tools

### 13.1 Online Platforms

| Platform | URL | Features |
|----------|-----|---------|
| 神机阁 | shenjige.cn/ziwei | Free chart + AI interpretation |
| 星尘算命 | kvov.com | Free chart, detailed star explanations |
| 华易网 | k366.com/ziwei | Free chart, mobile-friendly |

### 13.2 iztro Library (Open Source)

The **iztro** library (JavaScript/TypeScript, used by Vietnamese py-iztro) documents all star placement rules at: https://iztro.com/learn/setup

This is the most authoritative open-source implementation of the 安星诀.

### 13.3 Key Reference Texts

- 《紫微斗数全书》 (Complete Zi Wei Dou Shu Classic) — attributed to 陈希夷
- 《紫微斗数太微赋》 — Classic interpretive text
- 王亭之 commentary series — modern standard reference

---

## Summary: Key Differences from Vietnamese Tử Vi

| Aspect | Chinese 紫微斗数 | Vietnamese Tử Vi |
|--------|----------------|-----------------|
| Star count | 108 stars total | Typically uses subset (~50-60 commonly) |
| 四化 layers | Multiple (natal + period + annual + palace) | Usually only natal 四化 |
| 飞化 | Advanced technique used by professionals | Rarely used |
| Scoring | Some apps use point-based scoring | Not standard |
| 长生十二神 | Full 12-stage cycle | Partial — mainly 长生/帝旺/墓 noted |
| 博士/将前/岁前 12 gods | All three groups used | Often simplified |
| 宫干 system | Essential for 飞化 | Used in traditional charts |

---

## Sources

- [紫微斗数108颗星曜(全) — 紫微取象派](https://www.ziweishuyuan.com/discussion/242.html)
- [紫微斗数诸星分级及分类 — 华腾智算博客园](https://www.cnblogs.com/xiongwei/p/9816948.html)
- [紫微斗数安星诀 — iztro.com](https://iztro.com/learn/setup)
- [紫微斗数算法实现流程 — 博客园](https://www.cnblogs.com/voidobject/p/18510346)
- [天干四化表 — vocus.cc](https://vocus.cc/article/6646c651fd89780001ef63be)
- [紫微斗数十天干禄权科忌四化表 — 知乎](https://zhuanlan.zhihu.com/p/638973158)
- [紫微斗数庙旺平陷的意义及用法 — 玄门信息咨询](https://www.xuanmen.com.cn/archives/444.html)
- [星曜庙旺平陷表 — 令东来](https://www.xuanmen.com.cn/archives/101.html)
- [紫微斗数命主和身主 — 博客园](https://www.cnblogs.com/live41/p/4127477.html)
- [紫微斗数是如何排盘的8个步骤 — 知乎](https://zhuanlan.zhihu.com/p/678994105)
- [太岁十二神/博士十二神 — 知乎](https://zhuanlan.zhihu.com/p/710116775)
- [紫微斗数将前十二神煞 — 知乎](https://zhuanlan.zhihu.com/p/623329187)
- [紫微斗数大限小限流年 — 知乎](https://zhuanlan.zhihu.com/p/718987833)
- [四化飞星活用例解 — 星尘算命](http://m-zw.kvov.com/sswzx.php?id=5323333666655550303)
- [紫微斗数飞宫体系 — CSDN](https://blog.csdn.net/u011619323/article/details/136129058)
- [紫微斗数命主身主命宫身宫 — 神机阁](https://www.shenjige.cn/details/czrDpeWid.html)
- [紫微斗数中诸星分类分级 — 紫微取象派](https://www.ziweishuyuan.com/introduction/ziwei-foundation/208.html)
