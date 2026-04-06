# Tử Vi — Lập Lá Số (An Sao, Cung Mệnh, Phụ Tinh, Vận Hạn)

> Nguồn: "58_TU_VI_THUC_HANH.pdf" — Phần kiến thức lập lá số, an sao, tính cục, vận hạn.

---

## 1. AN CUNG MỆNH VÀ CUNG THÂN

### 1.1. Cung Mệnh
- **Bước 1**: Lấy cung **Dần** = tháng Giêng, tính **thuận** đến tháng sinh → cung A
- **Bước 2**: Từ cung A gọi là giờ **Tý**, tính **nghịch** đến giờ sinh → cung Mệnh

### 1.2. Cung Thân
- **Bước 1**: Giống bước 1 trên → cung A
- **Bước 2**: Từ cung A gọi là giờ **Tý**, tính **thuận** đến giờ sinh → cung Thân

### 1.3. Cung An Thân — Quy tắc đồng cung
Cung Thân **không phải cung độc lập** — luôn đồng cung với 1 trong 6 cung sau, dựa vào giờ sinh:

| Giờ sinh (địa chi) | Đồng cung với |
|--------------------|--------------|
| Tý, Ngọ | Mệnh |
| Tỵ, Hợi | Phu Thê |
| Thìn, Tuất | Tài Bạch |
| Mão, Dậu | Thiên Di |
| Dần, Thân | Quan Lộc |
| Sửu, Mùi | Phúc Đức |

**Hiển thị trong lá số:** Thêm tag `<THÂN>` đỏ đậm ngay sau tên cung.  
Ví dụ: người sinh giờ Tý → cung Mệnh hiển thị **MỆNH `<THÂN>`**

**Implement (frontend):**
- `isThan = palace.dia_chi === thanDiaChi` (không loại trừ isMenh)
- Khi `isMenh && isThan` → thêm class `menh-than` (viền vàng + silver inner glow)
- Header cung: `${cungName}<span class="palace-than-tag">&lt;THÂN&gt;</span>`
- CSS `.palace-than-tag`: `font-size:1em`, `color:#E53935`, `font-weight:700`

### 1.4. Âm Dương Nam Nữ
Xác định dựa vào **Can năm sinh** và **giới tính**:

| Can năm | Âm/Dương |
|---------|----------|
| Giáp, Bính, Mậu, Canh, Nhâm | DƯƠNG |
| Ất, Đinh, Kỷ, Tân, Quý | ÂM |

Kết hợp với giới tính → 4 loại: **DƯƠNG NAM / ÂM NAM / DƯƠNG NỮ / ÂM NỮ**

Ý nghĩa: dùng để xác định chiều thuận/nghịch khi an sao (đại hạn đi thuận hay nghịch).

**Hiển thị:** Dòng in đậm ngay dưới "Thân Chủ" trong ô chính giữa lá số.

**Implement (frontend `buildCenterPanelHTML`):**
```js
const _DUONG_CAN = new Set(['Giáp', 'Bính', 'Mậu', 'Canh', 'Nhâm']);
const yearCan = data.birth?.can_chi?.year?.split(' ')[0] || '';
const isDuong = _DUONG_CAN.has(yearCan);
const isNam   = gender.includes('nam') || gender === 'male';
// → "DƯƠNG NAM" / "ÂM NỮ" ...
```

---

## 2. XÁC ĐỊNH CỤC

### 2.1. Tháng Giêng theo Can năm (Ngũ Hổ Độn)
| Can năm | Tháng Giêng |
|---------|------------|
| Giáp, Kỷ | Bính Dần |
| Ất, Canh | Mậu Dần |
| Bính, Tân | Canh Dần |
| Đinh, Nhâm | Nhâm Dần |
| Mậu, Quý | Giáp Dần |

### 2.2. Cục
Lấy Can tháng Giêng, đánh từ Dần xuôi đến cung an Mệnh → ngũ hành của Nạp Âm = Cục:

| Cục | Tên | Vòng Tràng Sinh bắt đầu | Đại Hạn bắt đầu |
|-----|-----|--------------------------|-----------------|
| Thủy Nhị Cục | Nước 2 | Thân | 2 tuổi |
| Mộc Tam Cục | Mộc 3 | Hợi | 3 tuổi |
| Kim Tứ Cục | Kim 4 | Tỵ | 4 tuổi |
| Thổ Ngũ Cục | Thổ 5 | Thân | 5 tuổi |
| Hỏa Lục Cục | Lửa 6 | Dần | 6 tuổi |

---

## 3. AN 14 CHÍNH TINH

### 3.1. Vòng Tử Vi (6 sao, đi nghịch từ cung Tử Vi)
- Tử Vi → (nghịch 1) Thiên Cơ → (bỏ 1) → Thái Dương, Vũ Khúc, Thiên Đồng (cùng cung) → (bỏ 2) → Liêm Trinh

### 3.2. Vòng Thiên Phủ (8 sao, đi thuận từ cung Thiên Phủ)
Thiên Phủ luôn đối xứng Tử Vi qua trục Dần–Thân
- Thiên Phủ → Thái Âm → Tham Lang → Cự Môn → Thiên Tướng → Thiên Lương → Thất Sát → (bỏ 3) → Phá Quân

---

## 4. BẢNG CƯỜNG ĐỘ 14 CHÍNH TINH

### TỬ VI (Thổ)
| Miếu | Vượng | Đắc | Bình Hòa | Hãm |
|------|-------|-----|----------|-----|
| Tý, Ngọ, Dần, Thân | Thìn, Tuất | Sửu, Mùi | Tỵ, Hợi, Mão, Dậu | — |

### THIÊN CƠ (Mộc)
| Miếu | Vượng | Đắc | Bình Hòa | Hãm |
|------|-------|-----|----------|-----|
| Tý, Ngọ | Mão, Dậu | Dần, Thân | Thìn, Tuất, Tỵ, Hợi | Sửu, Mùi |

### THÁI DƯƠNG (Dương Hỏa)
| Miếu | Vượng | Bình Hòa | Hãm |
|------|-------|----------|-----|
| Mão | Ngọ, Tỵ, Thìn, Dần | Dậu, Mùi, Thân | Tuất, Hợi, Tý, Sửu |

### VŨ KHÚC (Kim)
| Miếu | Đắc | Bình Hòa | Hãm |
|------|-----|----------|-----|
| Thìn, Tuất, Sửu, Mùi | Dần, Thân, Mão, Dậu | Tý, Ngọ | Tỵ, Hợi |

### THIÊN ĐỒNG (Thủy đới Thổ)
| Miếu | Vượng | Đắc | Bình Hòa | Hãm |
|------|-------|-----|----------|-----|
| Tỵ, Hợi | Tý, Thân | Dần | Mão, Dậu, Tuất, Thìn | Ngọ, Mùi, Sửu |

### LIÊM TRINH (Âm Hỏa)
| Miếu | Vượng | Hãm |
|------|-------|-----|
| Dần, Thân, Tý, Ngọ | Thìn, Tuất, Sửu, Mùi | Tỵ, Hợi, Mão, Dậu |

### THIÊN PHỦ (Âm Thổ)
| Miếu | Vượng | Đắc |
|------|-------|-----|
| Sửu, Mùi, Thìn, Tuất, Mão | Tý, Ngọ | Dậu, Tỵ, Hợi, Dần, Thân |

*(Không có cung Hãm)*

### THÁI ÂM (Âm Thủy)
| Miếu | Vượng | Đắc | Hãm |
|------|-------|-----|-----|
| Hợi, Tý, Sửu | Dậu, Tuất | Mùi, Thân | Dần, Mão, Thìn, Tỵ, Ngọ |

### THAM LANG (Âm Thủy)
| Miếu | Đắc | Bình Hòa | Hãm |
|------|-----|----------|-----|
| Sửu, Mùi, Thìn, Tuất | Dần, Thân | Tý, Ngọ | Mão, Dậu, Tỵ, Hợi |

### CỰ MÔN (Âm Thủy)
| Miếu | Vượng | Đắc | Hãm |
|------|-------|-----|-----|
| Mão, Dậu | Tý, Ngọ, Dần | Thân, Hợi | Thìn, Tuất, Sửu, Mùi, Tỵ |

### THIÊN TƯỚNG (Dương Thủy)
| Miếu | Vượng | Đắc | Hãm |
|------|-------|-----|-----|
| Dần, Thân | Tý, Ngọ, Tuất, Thìn | Tỵ, Hợi, Sửu, Mùi | Mão, Dậu |

### THIÊN LƯƠNG (Âm Thổ đới Mộc)
| Miếu | Vượng | Đắc | Hãm |
|------|-------|-----|-----|
| Ngọ, Tuất, Thìn | Tý, Mão, Dần, Thân | Mùi, Sửu | Tỵ, Hợi, Dậu |

### THẤT SÁT (Dương Kim đới Hỏa)
| Miếu | Vượng | Đắc | Hãm |
|------|-------|-----|-----|
| Dần, Thân, Tý, Ngọ | Tỵ, Hợi | Sửu, Mùi | Mão, Dậu, Thìn, Tuất |

### PHÁ QUÂN (Âm Thủy)
| Miếu | Vượng | Đắc | Bình Hòa | Hãm |
|------|-------|-----|----------|-----|
| Tý, Ngọ | Mùi, Sửu | Thìn, Tuất | Tỵ, Hợi | Dần, Thân, Mão, Dậu |

---

## 5. AN CÁC SAO PHỤ TINH

### 5.1. Lộc Tồn (an theo Can năm sinh)
| Can | Cung |
|-----|------|
| Giáp | Dần |
| Ất | Mão |
| Bính, Mậu | Tỵ |
| Đinh, Kỷ | Ngọ |
| Canh | Thân |
| Tân | Dậu |
| Nhâm | Hợi |
| Quý | Tý |

### 5.2. Kình Dương & Đà La (tính từ Lộc Tồn)
- **Kình Dương**: cung **tiếp theo thuận** sau Lộc Tồn 1 cung
- **Đà La**: cung **trước** Lộc Tồn 1 cung (nghịch 1)

**Cường độ Kình Dương**: Đắc: Thìn, Tuất, Sửu, Mùi | Hãm: Tý, Ngọ, Mão, Dậu, Dần, Tỵ, Thân, Hợi
**Cường độ Đà La**: Đắc: Thìn, Tuất, Sửu, Mùi | Hãm: các cung còn lại

### 5.3. Thiên Khôi – Thiên Việt (an theo Can năm)
| Can | Thiên Khôi | Thiên Việt |
|-----|-----------|-----------|
| Giáp, Mậu | Sửu | Mùi |
| Ất, Kỷ | Tý | Thân |
| Bính, Đinh | Hợi | Dậu |
| Canh, Tân | Ngọ | Dần |
| Nhâm, Quý | Mão | Tỵ |

### 5.4. Văn Xương – Văn Khúc (an theo giờ sinh)
- **Văn Xương**: lấy cung **Tuất** = giờ Tý, tính **nghịch** đến giờ sinh
- **Văn Khúc**: lấy cung **Thìn** = giờ Tý, tính **thuận** đến giờ sinh

### 5.5. Tả Phụ – Hữu Bật (an theo tháng sinh âm lịch)
- **Tả Phụ**: lấy cung **Thìn** = tháng Giêng, tính **thuận** đến tháng sinh
- **Hữu Bật**: lấy cung **Tuất** = tháng Giêng, tính **nghịch** đến tháng sinh

### 5.6. Thiên Mã (an theo Chi năm sinh)
| Chi năm | Thiên Mã |
|---------|---------|
| Dần, Ngọ, Tuất | Thân |
| Thân, Tý, Thìn | Dần |
| Tỵ, Dậu, Sửu | Hợi |
| Hợi, Mão, Mùi | Tỵ |

### 5.7. Hỏa Tinh – Linh Tinh (an theo Chi năm + giờ sinh)

**Điểm khởi:**
| Chi năm | Hỏa Tinh khởi | Linh Tinh khởi |
|---------|--------------|---------------|
| Dần, Ngọ, Tuất | Sửu | Mão |
| Thân, Tý, Thìn | Dần | Tuất |
| Tỵ, Dậu, Sửu | Mão | Tuất |
| Hợi, Mão, Mùi | Dậu | Tuất |

**Chiều di chuyển** (lấy điểm khởi = giờ Tý, tính đến giờ sinh):
- **Dương Nam / Âm Nữ**: Hỏa Tinh đi **thuận**, Linh Tinh đi **nghịch**
- **Âm Nam / Dương Nữ**: Hỏa Tinh đi **nghịch**, Linh Tinh đi **thuận**

> Dương Can: Giáp, Bính, Mậu, Canh, Nhâm | Âm Can: Ất, Đinh, Kỷ, Tân, Quý

**Cường độ Hỏa Tinh:**
| Miếu | Đắc | Bình Hòa (Lợi địa) | Hãm |
|------|-----|---------------------|-----|
| Dần, Ngọ, Tuất | Tỵ, Dậu, Sửu | Hợi, Mão, Mùi | Thân, Tý, Thìn |

**Cường độ Linh Tinh:**
| Miếu | Bình Hòa | Hãm |
|------|----------|-----|
| Dần, Tuất, Thìn, Tỵ, Mùi | Tý, Ngọ, Thân, Mão | Dậu, Sửu, Hợi |

### 5.8. Địa Kiếp – Địa Không (an theo giờ sinh)
Lấy cung **Hợi** = giờ Tý:
- **Địa Kiếp**: tính **thuận** đến giờ sinh
- **Địa Không**: tính **nghịch** đến giờ sinh

### 5.9. Hồng Loan – Thiên Hỷ (an theo Chi năm sinh)
- **Hồng Loan**: lấy cung **Mão** = Chi Tý, tính **nghịch** đến Chi năm sinh
- **Thiên Hỷ**: an ở cung **xung** với Hồng Loan (đối diện)

### 5.10. Thiên La – Địa Võng (cố định)
- **Thiên La**: luôn ở cung **Thìn**
- **Địa Võng**: luôn ở cung **Tuất**

> ⚠️ **Implementation note (v44)**: Thiên La và Địa Võng **KHÔNG CÓ** trong danh sách "an sao tu vi.pdf". Đã **xóa** khỏi implementation, không hiển thị trên lá số.

### 5.11. Thiên Hình – Thiên Diêu – Thiên Y (an theo tháng sinh âm lịch)
- **Thiên Hình**: lấy cung **Dậu** = tháng Giêng, tính **thuận** đến tháng sinh
- **Thiên Diêu / Thiên Y**: lấy cung **Sửu** = tháng Giêng, tính **thuận** đến tháng sinh

### 5.12. Thiên Khốc – Thiên Hư (an theo Chi năm sinh)
- **Thiên Khốc**: lấy cung **Ngọ** = Chi Tý, tính **nghịch** đến Chi năm sinh
- **Thiên Hư**: lấy cung **Ngọ** = Chi Tý, tính **thuận** đến Chi năm sinh

### 5.13. Hồng Loan – Thiên Hỷ theo Chi năm
*(Đã ghi ở 5.9 — tính theo Chi năm sinh, không phải tháng)*

### 5.14. Đào Hoa (an theo Chi năm sinh)
Bảng tra từng chi (nguồn: an sao tu vi.pdf):

| Chi năm | Đào Hoa | Chi năm | Đào Hoa |
|---------|--------|---------|--------|
| Tý | Dậu | Ngọ | Mão |
| Sửu | Ngọ | Mùi | Tý |
| Dần | Mão | Thân | Dậu |
| Mão | Tý | Dậu | Ngọ |
| Thìn | Dậu | Tuất | Mão |
| Tỵ | Ngọ | Hợi | Tý |

### 5.15. Hoa Cái (an theo Chi năm sinh)
| Chi năm | Hoa Cái |
|---------|--------|
| Dần, Ngọ, Tuất | Tuất |
| Thân, Tý, Thìn | Thìn |
| Tỵ, Dậu, Sửu | Sửu |
| Hợi, Mão, Mùi | Mùi |

### 5.16. Cô Thần – Quả Tú (an theo Chi năm sinh)
| Chi năm | Cô Thần | Quả Tú |
|---------|---------|--------|
| Dần, Mão, Thìn | Tỵ | Sửu |
| Tỵ, Ngọ, Mùi | Thân | Thìn |
| Thân, Dậu, Tuất | Hợi | Mùi |
| Hợi, Tý, Sửu | Dần | Tuất |

### 5.17. Kiếp Sát (an theo Chi năm sinh)
Bảng tra từng chi (nguồn: an sao tu vi.pdf):

| Chi năm | Kiếp Sát | Chi năm | Kiếp Sát |
|---------|---------|---------|---------|
| Tý | Tỵ | Ngọ | Hợi |
| Sửu | Dần | Mùi | Thân |
| Dần | Hợi | Thân | Tỵ |
| Mão | Thân | Dậu | Dần |
| Thìn | Tỵ | Tuất | Hợi |
| Tỵ | Dần | Hợi | Thân |

### 5.18. Phá Toái (an theo Chi năm sinh)
| Chi năm | Phá Toái |
|---------|---------|
| Tý, Ngọ, Mão, Dậu | Tỵ |
| Dần, Thân, Tỵ, Hợi | Dậu |
| Thìn, Tuất, Sửu, Mùi | Sửu |

### 5.19. Triệt Lộ Không Vong (2 cung, theo Can năm)
| Can năm | 2 cung Triệt Lộ |
|---------|----------------|
| Giáp, Kỷ | Dậu, Thân |
| Ất, Canh | Mùi, Ngọ |
| Bính, Tân | Thìn, Tỵ |
| Đinh, Nhâm | Mão, Dần |
| Mậu, Quý | Sửu, Tý |

### 5.20. Tuần Không (2 cung, theo Con Giáp năm sinh)
| Con Giáp | 2 cung Tuần Không |
|----------|------------------|
| Giáp Dần | Tý, Sửu |
| Giáp Thìn | Dần, Mão |
| Giáp Ngọ | Thìn, Tỵ |
| Giáp Thân | Ngọ, Mùi |
| Giáp Tuất | Thân, Dậu |
| Giáp Tý | Tuất, Hợi |

### 5.21. Ân Quang – Thiên Quý (an theo ngày sinh)
- **Ân Quang**: lấy cung Văn Xương = ngày 1, tính **thuận** đến ngày sinh → lùi 1 cung
- **Thiên Quý**: lấy cung Văn Khúc = ngày 1, tính **nghịch** đến ngày sinh → lùi 1 cung

### 5.22. Tam Thai – Bát Tọa (an theo ngày sinh)
- **Tam Thai**: lấy cung Tả Phụ = ngày 1, tính **thuận** đến ngày sinh
- **Bát Tọa**: lấy cung Hữu Bật = ngày 1, tính **nghịch** đến ngày sinh

### 5.23. Long Trì – Phượng Các – Giải Thần (an theo Chi năm)
- **Long Trì**: lấy cung **Thìn** = Chi Tý, tính **thuận** đến Chi năm
- **Phượng Các**: lấy cung **Tuất** = Chi Tý, tính **nghịch** đến Chi năm
- **Giải Thần**: đồng cung với Phượng Các

### 5.24. Thiên Phúc – Thiên Quan (an theo Can năm)
| Can | Thiên Phúc | Thiên Quan |
|-----|-----------|-----------|
| Giáp | Dậu | Mùi |
| Ất | Thân | Thìn |
| Bính | Tý | Tỵ |
| Đinh | Hợi | Dần |
| Mậu | Mão | Mão |
| Kỷ | Dần | Dậu |
| Canh | Ngọ | Hợi |
| Tân | Tỵ | Dậu |
| Nhâm | Ngọ | Tuất |
| Quý | Tỵ | Ngọ |

### 5.25. Thiên Đức – Nguyệt Đức (an theo Chi năm)
- **Thiên Đức**: lấy cung **Dậu** = Chi Tý, tính **thuận** đến Chi năm
- **Nguyệt Đức**: lấy cung **Tỵ** = Chi Tý, tính **thuận** đến Chi năm

### 5.26. Thiên Tài – Thiên Thọ (an theo Chi năm)
- **Thiên Tài**: lấy cung **Mệnh** = Chi Tý, tính **thuận** đến Chi năm
- **Thiên Thọ**: lấy cung **Thân** = Chi Tý, tính **thuận** đến Chi năm

### 5.27. Thiên Y – Thiên Giải – Địa Giải (an theo tháng sinh âm lịch)
Bảng tra theo tháng (nguồn: an sao tu vi.pdf):

| Tháng | Thiên Y | Thiên Giải | Địa Giải |
|-------|---------|-----------|---------|
| 1 | Sửu | Thân | Mùi |
| 2 | Dần | Dậu | Thân |
| 3 | Mão | Tuất | Dậu |
| 4 | Thìn | Hợi | Tuất |
| 5 | Tỵ | Tý | Hợi |
| 6 | Ngọ | Sửu | Tý |
| 7 | Mùi | Dần | Sửu |
| 8 | Thân | Mão | Dần |
| 9 | Dậu | Thìn | Mão |
| 10 | Tuất | Tỵ | Thìn |
| 11 | Hợi | Ngọ | Tỵ |
| 12 | Tý | Mùi | Ngọ |

### 5.28. Thiên Hình – Thiên Không (an cố định theo Thái Tuế)
- **Thiên Không**: an ngay cung **tiếp theo thuận** sau cung Thái Tuế 1 cung

### 5.29. Thiên Thương – Thiên Sứ (cố định theo cung)
- **Thiên Thương**: an ngay cung **Nô Bộc**
- **Thiên Sứ**: an ngay cung **Tật Ách**

### 5.30. Các sao theo Thiên Can năm (nguồn: an sao tu vi.pdf)

| Can | Lưu Hà | Quốc Ấn | Đường Phù | Văn Tinh | Thiên Trù |
|-----|--------|---------|----------|---------|----------|
| Giáp | Dậu | Tuất | Mùi | Tỵ | Tỵ |
| Ất | Tuất | Hợi | Thân | Ngọ | Ngọ |
| Bính | Mùi | Sửu | Tuất | Thân | Tý |
| Đinh | Thìn | Dần | Hợi | Dậu | Tỵ |
| Mậu | Tỵ | Sửu | Tuất | Thân | Ngọ |
| Kỷ | Ngọ | Dần | Hợi | Dậu | Thân |
| Canh | Thân | Thìn | Sửu | Hợi | Dần |
| Tân | Mão | Tỵ | Dần | Tý | Ngọ |
| Nhâm | Hợi | Mùi | Thìn | Dậu | Dậu |
| Quý | Dần | Thân | Tỵ | Mão | Tuất |

> **Hành màu**: Lưu Hà=Thủy, Quốc Ấn=Kim, Đường Phù=Thổ, Văn Tinh=Mộc

---

## 6. TỨ HÓA (an theo Can năm sinh)

| Can | Hóa Lộc | Hóa Quyền | Hóa Khoa | Hóa Kỵ |
|-----|---------|-----------|---------|--------|
| Giáp | Liêm Trinh | Phá Quân | Vũ Khúc | Thái Dương |
| Ất | Thiên Cơ | Thiên Lương | Tử Vi | Thái Âm |
| Bính | Thiên Đồng | Thiên Cơ | Văn Xương | Liêm Trinh |
| Đinh | Thái Âm | Thiên Đồng | Thiên Cơ | Cự Môn |
| Mậu | Tham Lang | Thái Âm | Hữu Bật | Thiên Cơ |
| Kỷ | Vũ Khúc | Tham Lang | Thiên Lương | Văn Khúc |
| Canh | Thái Dương | Vũ Khúc | Thiên Đồng | Thái Âm |
| Tân | Vũ Khúc | Thái Dương | Văn Khúc | Văn Xương |
| Nhâm | Thiên Lương | Tử Vi | Thiên Phủ | Vũ Khúc |
| Quý | Phá Quân | Cự Môn | Thái Âm | Tham Lang |

---

## 7. BA VÒNG SAO

### 7.1. Vòng Thái Tuế (12 sao)
**An từ Chi năm sinh** (Thái Tuế = cung Chi đó), đi **thuận**:

| STT | Tên sao | Tính chất |
|-----|---------|-----------|
| 1 | Thái Tuế | Hung |
| 2 | Thiếu Dương | Trung |
| 3 | Tang Môn | Hung |
| 4 | Thiếu Âm | Trung |
| 5 | Quan Phủ | Hung |
| 6 | Tử Phù | Hung |
| 7 | Tuế Phá | Hung |
| 8 | Long Đức | Cát |
| 9 | Bạch Hổ | Hung |
| 10 | Phúc Đức | Cát |
| 11 | Điếu Khách | Hung |
| 12 | Trực Phù | Hung |

### 7.2. Vòng Tràng Sinh (12 sao)
**Điểm khởi** theo Cục (xem bảng mục 2.2), chiều đi theo **Dương/Âm + Nam/Nữ**:
- **Dương Nam, Âm Nữ**: đi **thuận**
- **Âm Nam, Dương Nữ**: đi **nghịch**

| STT | Tên sao |
|-----|---------|
| 1 | Tràng Sinh |
| 2 | Mộc Dục |
| 3 | Quan Đới |
| 4 | Lâm Quan |
| 5 | Đế Vượng |
| 6 | Suy |
| 7 | Bệnh |
| 8 | Tử |
| 9 | Mộ |
| 10 | Tuyệt |
| 11 | Thai |
| 12 | Dưỡng |

### 7.3. Vòng Bác Sĩ / Vòng Lộc Tồn (12 sao)
**An từ cung Lộc Tồn** (Bác Sĩ = cung Lộc Tồn), chiều đi giống Vòng Tràng Sinh:
- **Dương Nam, Âm Nữ**: đi **thuận**
- **Âm Nam, Dương Nữ**: đi **nghịch**

| STT | Tên sao | Tính chất |
|-----|---------|-----------|
| 1 | Bác Sĩ | Cát |
| 2 | Lực Sĩ | Cát |
| 3 | Thanh Long | Cát |
| 4 | Tiểu Hao | Hung |
| 5 | Tướng Quân | Cát |
| 6 | Tấu Thư | Cát |
| 7 | Phi Liêm | Hung |
| 8 | Hỷ Thần | Cát |
| 9 | Bệnh Phù | Hung |
| 10 | Đại Hao | Hung |
| 11 | Phục Binh | Hung |
| 12 | Quan Phủ | Hung |

---

## 8. ĐẠI HẠN VÀ TIỂU HẠN

### 8.1. Đại Hạn
- Mỗi hạn = **10 năm**, bắt đầu từ tuổi = số Cục
- Chiều: **Dương Nam / Âm Nữ** đi **thuận** | **Âm Nam / Dương Nữ** đi **nghịch**

### 8.2. Tiểu Hạn
- Đàn ông: chiều **thuận** | Đàn bà: chiều **nghịch**
- Điểm bắt đầu (tuổi 1) theo Chi năm:

| Chi năm | Tiểu Hạn tuổi 1 |
|---------|----------------|
| Dần, Ngọ, Tuất | Thìn |
| Thân, Tý, Thìn | Tuất |
| Tỵ, Dậu, Sửu | Mùi |
| Hợi, Mão, Mùi | Sửu |

---

## 9. QUY TẮC PHÂN LOẠI SAO TỐT / XẤU

> **Cập nhật lần cuối**: v56 (2026-04-02)
> **Quy tắc màu**: 🔴 đỏ = Hỏa | 🟢 xanh = Mộc | ⚫ đen = Thủy | 🟡 vàng = Thổ | ⬜ xám = Kim
> **Hiển thị**: Sao tốt ở cột trái, sao xấu ở cột phải. Tuần Không/Triệt Lộ luôn cuối cột xấu.
> **Format đặc biệt**: Triệt Lộ = nền đen chữ trắng | Tuần Không = nền đỏ chữ trắng

### 9.1. Hành của các sao phụ tinh (nguồn xác nhận)

#### ⬜ Kim
| Sao | Ghi chú |
|-----|---------|
| Văn Xương | Tiểu hạn |
| Hóa Khoa | Tứ Hóa |
| Thai Phụ | Vòng giờ |
| Hoa Cái | Địa chi năm |
| Quan Đới | Vòng Tràng Sinh |
| Lâm Quan | Vòng Tràng Sinh |
| Đế Vượng | Vòng Tràng Sinh |
| Tấu Thư | Vòng Bác Sĩ |
| Bạch Hổ | Vòng Thái Tuế |
| Kình Dương | Thiên can năm |
| Đà La | Thiên can năm |
| Linh Tinh | Giờ + cục |
| Thiên La | Cố định tại Thìn |
| Địa Võng | Cố định tại Tuất |

#### 🟢 Mộc
| Sao | Ghi chú |
|-----|---------|
| Hóa Lộc | Tứ Hóa |
| Phượng Các | Địa chi năm |
| Ân Quang | Từ Văn Xương + ngày |
| Bát Tọa | Từ Hữu Bật + ngày |
| Đào Hoa | Địa chi năm |
| Giải Thần | Địa chi năm (nghịch từ Dần) |
| Đường Phù | Thiên can năm |
| Tướng Quân | Vòng Bác Sĩ |
| Tang Môn | Vòng Thái Tuế |
| Cô Thần | Địa chi năm |
| Quả Tú | Địa chi năm |

#### ⚫ Thủy
| Sao | Ghi chú |
|-----|---------|
| Văn Khúc | Tiểu hạn |
| Hữu Bật | Thiên can năm |
| Hóa Kỵ | Tứ Hóa |
| Long Trì | Địa chi năm |
| Thiên Quý | Từ Văn Khúc - ngày |
| Tam Thai | Từ Tả Phụ + ngày |
| Hồng Loan | Địa chi năm |
| Thiên Hỷ | Địa chi năm |
| Thanh Long | Vòng Bác Sĩ |
| Long Đức | Vòng Thái Tuế |
| Tràng Sinh | Vòng Tràng Sinh |
| Mộc Dục | Vòng Tràng Sinh |
| Suy | Vòng Tràng Sinh |
| Tử | Vòng Tràng Sinh |
| Bác Sĩ | Vòng Bác Sĩ |
| Thiếu Âm | Vòng Thái Tuế |
| Thiên Khốc | Địa chi năm |
| Thiên Hư | Địa chi năm |
| Thiên Diêu | Tháng sinh |
| Thiên Y | Tháng sinh |
| Lưu Hà | Thiên can năm |
| Thiên Sứ | Cung Tật Ách |

#### 🔴 Hỏa
| Sao | Ghi chú |
|-----|---------|
| Thiên Khôi | Thiên can năm |
| Thiên Việt | Thiên can năm |
| Thiên Mã | Địa chi năm |
| Thiên Quan | Thiên can năm |
| Thiên Giải | Tháng sinh |
| Thiên Đức | Tháng sinh |
| Nguyệt Đức | Tháng sinh |
| Bệnh | Vòng Tràng Sinh |
| Lực Sĩ | Vòng Bác Sĩ |
| Đại Hao | Vòng Bác Sĩ |
| Tiểu Hao | Vòng Bác Sĩ |
| Phi Liêm | Vòng Bác Sĩ |
| Hỷ Thần | Vòng Bác Sĩ |
| Thiếu Dương | Vòng Thái Tuế |
| Quan Phù | Vòng Thái Tuế (raw, trước remap) |
| Tử Phù | Vòng Thái Tuế (Tiểu Hao remap) |
| Trực Phù | Vòng Thái Tuế (Bệnh Phù remap) |
| Tuế Phá | Vòng Thái Tuế (Đại Hao remap) |
| Điếu Khách | Vòng Thái Tuế |
| Văn Tinh | Thiên can năm |
| Hỏa Tinh | Giờ + cục |
| Thiên Hình | Tháng sinh |
| Thiên Không | Địa chi năm (iztro) |
| Địa Không | Giờ sinh |
| Địa Kiếp | Giờ sinh |
| Kiếp Sát | Địa chi năm |
| Đẩu Quân | Năm→tháng nghịch→giờ thuận |
| Phá Toái | Địa chi năm |

#### 🟡 Thổ
| Sao | Ghi chú |
|-----|---------|
| Tả Phụ | Thiên can năm |
| Lộc Tồn | Thiên can năm |
| Hóa Quyền | Tứ Hóa |
| Phong Cáo | Giờ sinh |
| Thiên Phúc | Thiên can năm |
| Địa Giải | Tháng sinh |
| Phúc Đức | Vòng Thái Tuế (Thiên Đức remap) |
| Thiên Thọ | Tiểu hạn |
| Thiên Tài | Từ cung Mệnh + địa chi năm |
| Thiên Trù | Thiên can năm |
| Quốc Ấn | Thiên can năm |
| Mộ | Vòng Tràng Sinh |
| Thai | Vòng Tràng Sinh |
| Dưỡng | Vòng Tràng Sinh |
| Bệnh Phù | Vòng Bác Sĩ |
| Phục Binh | Vòng Bác Sĩ (伏兵) |
| Quan Phủ | Vòng Bác Sĩ (官府) |
| Thái Tuế | Vòng Thái Tuế (Tuế Kiến remap) |
| Thiên Thương | Cung Nô Bộc |

### 9.2. Phân loại sao tốt / xấu (BAD_STARS)

**Sao xấu** (hiển thị cột phải):
Kình Dương, Đà La, Hỏa Tinh, Linh Tinh, Địa Không, Địa Kiếp,
Thiên Hình, Thiên Diêu, Phá Toái, Phi Liêm, Thiên Khốc, Thiên Hư, Thiên Không,
Tiểu Hao, Đại Hao, Tử Phù, Tuế Phá,
Thái Tuế, Bạch Hổ, Tang Môn, Điếu Khách, Quan Phù, Quan Phủ, Bệnh Phù, Phục Binh,
Kiếp Sát, Cô Thần, Quả Tú, Tuần Không, Triệt Lộ,
Địa Võng, Thiên Thương, Thiên Sứ, Thiên La, Lưu Hà, Hóa Kỵ,
Tai Sát, Thiên Sát, Nguyệt Sát, Vong Thần

**Sao tốt**: tất cả còn lại

### 9.3. Hành của các cung theo Địa Chi

| Địa Chi | Hành | Âm Dương | Hiển thị |
|---------|------|----------|----------|
| Tý | Thủy | Dương | +THỦY |
| Sửu | Thổ | Âm | −THỔ |
| Dần | Mộc | Dương | +MỘC |
| Mão | Mộc | Âm | −MỘC |
| Thìn | Thổ | Dương | +THỔ |
| Tỵ | Hỏa | Âm | −HỎA |
| Ngọ | Hỏa | Dương | +HỎA |
| Mùi | Thổ | Âm | −THỔ |
| Thân | Kim | Dương | +KIM |
| Dậu | Kim | Âm | −KIM |
| Tuất | Thổ | Dương | +THỔ |
| Hợi | Thủy | Âm | −THỦY |

---

### 9.4. Trạng thái Đắc/Hãm của sao phụ tinh theo cung

> **Quy tắc hiển thị**: Đắc địa → **(Đ)** kế bên tên sao | Hãm địa → **(H)** kế bên tên sao | Còn lại → không ghi gì
> Miếu địa và Vượng địa được gộp vào **(Đ)**

| Sao | Đắc địa (Đ) | Hãm địa (H) |
|-----|-------------|-------------|
| Văn Xương | Tỵ, Dậu, Sửu (Miếu) · Thân, Tý, Thìn, Hợi (Đắc) | Dần, Ngọ, Tuất |
| Văn Khúc | Tỵ, Sửu, Dậu (Miếu) · Hợi, Mão, Mùi (Vượng) · Thân, Tý, Thìn (Đắc) | Ngọ, Tuất |
| Tả Phụ | Thìn, Tuất, Sửu, Mùi | — |
| Hữu Bật | Thìn, Tuất, Sửu, Mùi | — |
| Thiên Mã | Tỵ, Dần | — |
| Kình Dương | Thìn, Tuất, Sửu, Mùi | Tý, Ngọ, Mão, Dậu |
| Đà La | Thìn, Tuất, Sửu, Mùi | Dần, Thân, Tỵ, Hợi |
| Hỏa Tinh | Dần, Ngọ, Tuất (Miếu) · Tỵ, Dậu, Sửu, Hợi, Mão, Mùi (Đắc) | Thân, Tý, Thìn |
| Linh Tinh | Dần, Tuất, Thìn, Tỵ, Mùi (Miếu) | Dậu, Sửu, Hợi *(Tỵ có trong cả 2 → ưu tiên Miếu)* |
| Đại Hao | Dần, Thân, Mão, Dậu | Tý, Ngọ, Tỵ, Hợi |
| Tiểu Hao | Dần, Thân, Mão, Dậu | Tý, Ngọ, Tỵ, Hợi |
| Tang Môn | Dần, Thân, Mão, Dậu | — |
| Bạch Hổ | Dần, Thân, Mão, Dậu | — |
| Thiên Khốc | Tý, Ngọ (Miếu) · Mão, Dậu, Sửu, Mùi (Đắc) | — |
| Thiên Hư | Tý, Ngọ (Miếu) · Mão, Dậu, Sửu, Mùi (Đắc) | — |
| Thiên Hình | Dần, Thân, Mão, Dậu | — |
| Địa Không | Tỵ, Hợi, Dần, Thân | — |
| Địa Kiếp | Tỵ, Hợi, Dần, Thân | — |
| Thiên Diêu | Dần, Mão, Dậu, Tuất | — |

---

## 10. LƯU Ý QUAN TRỌNG KHI IMPLEMENT

1. **Tháng sinh dùng âm lịch** (không dùng dương lịch) cho tất cả các sao an theo tháng
2. **Hỏa Tinh / Linh Tinh**: phải tính đúng chiều (thuận/nghịch) theo Dương/Âm + Nam/Nữ
3. **Vòng Thái Tuế**: vị trí 6 là Tử Phù, vị trí 7 là Tuế Phá (không phải Tiểu Hao/Đại Hao)
4. **Thiên Phủ**: không có cung Hãm
5. **Lộc Tồn** = `lucunMin` trong iztro-py (禄存), không phải `lucreMin`
6. **Địa Kiếp** = `dijieMin` (地劫), không phải Địa Giải
7. **Chiều Dương/Âm**: Dương Can = Giáp, Bính, Mậu, Canh, Nhâm; Âm Can = Ất, Đinh, Kỷ, Tân, Quý

---

## 11. IMPLEMENTATION LOG

### v46 — Căn chỉnh vị trí trái/phải và màu sắc theo PDF
**Nguồn**: `dieu chinh cac sao phu tinh.pdf` — màu: xám=kim, đen=thủy, đỏ=hỏa, xanh=mộc, vàng=thổ

**BAD_STARS** (`tuvi-chart.js`):
- REMOVE: Trực Phù, Thiếu Âm, Phúc Bình (sai tên) → chuyển sang trái (tốt)
- ADD: Thái Tuế, Tử Phù, Tuế Phá, Thiên La, Phục Binh, Lưu Hà → phải (xấu)

**STAR_ELEMENT_MAP** — thay đổi đáng kể:
- Văn Xương: mộc → **kim** (xám trong PDF)
- Văn Khúc: kim → **thủy** (đen)
- Hồng Loan, Thiên Hỷ: hỏa → **thủy** (đen)
- Thiên Khôi, Thiên Việt, Phá Toái: kim → **hỏa** (đỏ)
- Lộc Tồn, Quốc Ấn: kim → **thổ** (vàng)
- Tả Phụ: mộc → **hỏa** (đỏ)
- Hữu Bật: mộc → **thủy** (đen)
- Thiên Y, Thiên Phúc, Thiên Quan, Thiên Tài, Giải Thần, Thiên Giải, Phượng Các, Văn Tinh: mộc → **hỏa** (đỏ)
- Địa Không, Địa Kiếp, Thiên Không: thủy → **thổ** (vàng)
- Cô Thần, Kiếp Sát, Phi Liêm: thổ → **hỏa** (đỏ)
- Tuần Không, Triệt Lộ: thổ → **thủy** (đen)
- Bát Tọa, Tam Thai: thổ → **thủy** (đen)
- Đẩu Quân: thổ → **hỏa** (đỏ)
- Địa Giải: thủy → **thổ** (vàng)
- Thiên Mã: thủy → **mộc** (xanh)
- Thiên Sứ: thổ → **thủy** (đen)
- Thêm mới: Hỷ Thần/hỏa, Phúc Đức/thổ, Thiên Đức/hỏa, Trực Phù/hỏa, Tướng Quân/hỏa, Thiếu Dương/hỏa, Lực Sĩ/hỏa, Bác Sĩ/thủy, Thanh Long/thủy, Thiếu Âm/thủy, Long Trì/thủy, Thiên Diêu/thủy, Thái Tuế/thủy, Tử Phù/thủy, Tuế Phá/thủy, Thiên La/hỏa, Phục Binh/hỏa, Bệnh Phù/thổ, v.v.

---

### v45 — Thêm 13 sao phụ theo VN formulas; sửa tên sao
**Thay đổi Python (`iztro_service.py`)**:
- Sửa tên: `fengge` → "Phượng Các" (không phải "Phong Các"), `bazuo` → "Bát Tọa"
- Xóa khỏi `ALLOWED_ADJ_STARS`: Giải Thần, Thiên Trù, Thiên Phúc, Thiên Quan, Thiên Không (iztro-py sai vị trí)
- Thêm 3 bảng tra Can: `_THIEN_TRU_BY_CAN`, `_THIEN_PHUC_BY_CAN`, `_THIEN_QUAN_BY_CAN`
- Thêm tự tính theo VN formula:
  - Giải Thần = đồng cung Phượng Các (§5.23)
  - Thiên Trù, Thiên Phúc, Thiên Quan (§5.24, §5.30)
  - Thiên Tài, Thiên Thọ theo Chi năm + Mệnh/Thân (§5.26)
  - Ân Quang = Văn Xương + ngày - 2 (§5.21)
  - Tam Thai = Tả Phụ + ngày - 1 (§5.22)
  - Bát Tọa = Hữu Bật - (ngày - 1) (§5.22)
  - Thiên Thương tại Nô Bộc, Thiên Sứ tại Tật Ách (§5.29)
  - Địa Võng cố định tại Tuất (§5.10)
  - Thiên Không = cung kế sau Thái Tuế (§5.28)

**Thay đổi JS (`tuvi-chart.js`)**:
- BAD_STARS: thêm `'Địa Võng', 'Thiên Thương', 'Thiên Sứ'`
- STAR_ELEMENT_MAP: thêm 7 sao mới

**Xóa**: Toàn bộ file cohoc (iztro_service_cohoc.py, lunar_service_cohoc.py, main_cohoc.py, TU_VI_COHOC_NOTES.md)

---

### v44 — Lọc phụ tinh theo "an sao tu vi.pdf"
**Nguồn thứ 2**: `/Users/duongrama/Desktop/an sao tu vi.pdf`

**Thay đổi Python (`iztro_service.py`)**:
- Thêm `ALLOWED_ADJ_STARS` — whitelist giữ lại đúng phụ tinh theo PDF
- Lọc `palace.adjective_stars` theo whitelist (bỏ ~14 sao không có trong PDF)
- Thêm bảng tra mới và tự tính 9 sao iztro-py không cung cấp:
  - **Theo Thiên Can**: Lưu Hà, Quốc Ấn, Đường Phù, Văn Tinh
  - **Theo Địa Chi**: Đào Hoa, Kiếp Sát
  - **Theo tháng âm lịch**: Thiên Y, Thiên Giải, Địa Giải
- Xóa inject Thiên La / Địa Võng (không có trong PDF)

**Thay đổi JS (`tuvi-chart.js`)**:
- Xóa `'Thiên La', 'Địa Võng'` khỏi `BAD_STARS`
- Thêm hành màu cho 9 sao mới vào `STAR_ELEMENT_MAP`

**Sao bị xóa khỏi lá số**:
Thiên Quý, Thiên Tài, Thiên Thọ, Thiên Thương, Thiên Sứ, Thiên Vu, Thiên Nguyệt, Tam Thai, Bát Tọa, Ân Quang, Hàm Trì, Niên Giải, Âm Sát, Bật Tọa, Thiên La, Địa Võng

### v43 — Redesign layout cung
- Header: can_chi abbr + tên cung + tuổi đại hạn
- Chính tinh: IN HOA + cường độ trong ngoặc
- Body 2 cột: sao tốt trái / sao xấu phải
- Footer: tràng sinh + hành đại vận

### v42 — Tô màu theo hành
- Kim=xám, Mộc=xanh lá, Thủy=đen xám, Hỏa=đỏ, Thổ=vàng cam

### v41 — VN_BRIGHTNESS_TABLE từ 2 file PDF
- `chinh tinh.pdf`: bảng đầy đủ Miếu/Vượng/Đắc/Bình Hòa/Hãm
- `mieudia.pdf`: ghi đè Miếu địa (ưu tiên)
- User sửa thủ công: Thiên Lương Miếu tại Thìn, Ngọ, Tuất

### v40 — Hỏa Tinh / Linh Tinh
- Tính đúng theo công thức Việt Nam (bỏ công thức Trung Quốc của iztro-py)
- Dương Nam/Âm Nữ: Hỏa thuận + Linh nghịch
- Âm Nam/Dương Nữ: Hỏa nghịch + Linh thuận

---
