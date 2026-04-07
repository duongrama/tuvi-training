# Nghiên Cứu Chuyên Sâu: Lá Số Tử Vi Việt Nam

> Ngày nghiên cứu: 2026-03-16
> Mục đích: Tài liệu kỹ thuật cho đội phát triển app Tử Vi

---

## MỤC LỤC

1. [Tổng Quan Hệ Thống](#1-tổng-quan-hệ-thống)
2. [14 Chính Tinh](#2-14-chính-tinh)
3. [Danh Sách Đầy Đủ Các Vòng Sao](#3-danh-sách-đầy-đủ-các-vòng-sao)
4. [Hệ Thống Miếu Vượng Đắc Bình Hãm](#4-hệ-thống-miếu-vượng-đắc-bình-hãm)
5. [Tứ Hóa Chi Tiết](#5-tứ-hóa-chi-tiết)
6. [Can Chi Từng Cung](#6-can-chi-từng-cung)
7. [Mệnh Chủ Và Thân Chủ](#7-mệnh-chủ-và-thân-chủ)
8. [Đại Hạn, Tiểu Hạn, Lưu Niên](#8-đại-hạn-tiểu-hạn-lưu-niên)
9. [Tuần và Triệt](#9-tuần-và-triệt)
10. [Hệ Thống Điểm Cung](#10-hệ-thống-điểm-cung)
11. [So Sánh Các App Tử Vi Nổi Tiếng](#11-so-sánh-các-app-tử-vi-nổi-tiếng)
12. [Nguồn Tham Khảo](#12-nguồn-tham-khảo)

---

## 1. TỔNG QUAN HỆ THỐNG

### Tử Vi Đẩu Số là gì?
Tử Vi Đẩu Số (紫微斗數) là hệ thống chiêm tinh học cổ điển của phương Đông. Tại Việt Nam, hệ thống này được gọi là Tử Vi. Lá số Tử Vi được lập dựa trên ngày, tháng, năm và giờ sinh âm lịch của người.

### Tổng Số Sao
Theo Trần Đoàn (người sáng lập), hệ thống gốc có **120 sao**. Sau khi được Việt hóa:
- **14 Chính Tinh** (sao chính, ảnh hưởng lớn nhất)
- **~97 Phụ Tinh** (sao phụ, cố định)
- **9 Lưu Tinh** (sao di động theo năm/hạn)
- **Tổng ~111-120 sao** tùy phái

### 12 Cung Cơ Bản
```
Mệnh | Phụ Mẫu | Phúc Đức | Điền Trạch
Quan Lộc | [Trung Tâm] | Tài Bạch
Nô Bộc | [Phái/Cục] | Tử Tức
Thiên Di | Tật Ách | Thê Thiếp | Huynh Đệ
```

12 cung: Mệnh, Huynh Đệ, Thê Thiếp, Tử Tức, Tài Bạch, Tật Ách, Thiên Di, Nô Bộc, Quan Lộc, Điền Trạch, Phúc Đức, Phụ Mẫu.

### Địa Chi Cố Định của 12 Cung
Địa chi của 12 cung trên thiên bàn là **cố định** (không phụ thuộc người):
- Vị trí cung **Mệnh** được xác định từ tháng sinh + giờ sinh
- Các cung còn lại đặt theo chiều **thuận** từ cung Mệnh

---

## 2. 14 CHÍNH TINH

### Nhóm Tử Vi Tinh Hệ (Bắc Đẩu - 6 sao)
| STT | Tên Sao | Ngũ Hành | Tính Chất Cơ Bản |
|-----|---------|----------|-----------------|
| 1 | Tử Vi | Thổ (Dương) | Đế vương, quyền lực, lãnh đạo |
| 2 | Thiên Cơ | Mộc (Âm) | Mưu lược, biến động, di chuyển |
| 3 | Thái Dương | Hỏa (Dương) | Quý nhân, công danh, nam giới |
| 4 | Vũ Khúc | Kim (Âm) | Tài lộc, quyết đoán, cô đơn |
| 5 | Thiên Đồng | Thủy (Dương) | Phúc lộc, hưởng thụ, hiền hòa |
| 6 | Liêm Trinh | Hỏa (Âm) | Nghiêm khắc, sắc bén, chính trực |

### Nhóm Thiên Phủ Tinh Hệ (Nam Đẩu - 8 sao)
| STT | Tên Sao | Ngũ Hành | Tính Chất Cơ Bản |
|-----|---------|----------|-----------------|
| 7 | Thiên Phủ | Thổ (Dương) | Phú quý, bền vững, tài chính |
| 8 | Thái Âm | Thủy (Âm) | Phụ nữ, tinh tế, tài lộc |
| 9 | Tham Lang | Thủy (Dương)/Mộc | Đa dạng, tham vọng, dục vọng |
| 10 | Cự Môn | Thủy (Âm) | Ngôn ngữ, thị phi, tối ám |
| 11 | Thiên Tướng | Thủy (Dương) | Ấn thụ, phụ tá, ngay thẳng |
| 12 | Thiên Lương | Thổ (Dương) | Phúc thọ, y dược, bảo hộ |
| 13 | Thất Sát | Kim (Âm) | Sát khí, võ tướng, đột phá |
| 14 | Phá Quân | Thủy (Âm) | Phá hoại, cải cách, khai phá |

### Vị Trí An Tử Vi (sao đầu hệ)
Tử Vi được an theo **Ngũ Hành Cục** và **ngày sinh âm lịch** (tra bảng an sao cụ thể theo từng cục).

---

## 3. DANH SÁCH ĐẦY ĐỦ CÁC VÒNG SAO

### 3.1 Vòng Tràng Sinh (12 sao)

**Khởi điểm theo Ngũ Hành Cục:**
| Cục | Tên Cục | Khởi Tràng Sinh Tại |
|-----|---------|-------------------|
| 2 | Thủy Nhị Cục | Thân |
| 3 | Mộc Tam Cục | Hợi |
| 4 | Kim Tứ Cục | Tị |
| 5 | Thổ Ngũ Cục | Thân |
| 6 | Hỏa Lục Cục | Dần |

**Chiều an sao:**
- Dương Nam + Âm Nữ → an **thuận chiều** (chiều kim đồng hồ)
- Âm Nam + Dương Nữ → an **nghịch chiều**

**12 vị trí của Vòng Tràng Sinh:**
| STT | Tên Sao | Ý Nghĩa Cốt Lõi |
|-----|---------|----------------|
| 1 | Trường Sinh | Khởi đầu, sinh mệnh, năng lượng mới |
| 2 | Mộc Dục | Tắm gội, non nớt, bất ổn, học hỏi |
| 3 | Quan Đới | Trưởng thành, danh phận, được công nhận |
| 4 | Lâm Quan | Đỉnh cao công danh, quyền lực |
| 5 | Đế Vượng | Cực thịnh, tự mãn, đỉnh điểm |
| 6 | Suy | Suy giảm, nghỉ ngơi, trầm tĩnh |
| 7 | Bệnh | Yếu đuối, bệnh tật, cần chăm sóc |
| 8 | Tử | Kết thúc, chuyển hóa, tử vong |
| 9 | Mộ | Tàng trữ, cất giấu, cuối cung |
| 10 | Tuyệt | Hoàn toàn đứt đoạn, trắng tay |
| 11 | Thai | Thai nghén, ẩn tàng, chuẩn bị |
| 12 | Dưỡng | Nuôi dưỡng, bảo bọc, hồi phục |

### 3.2 Vòng Lộc Tồn và Bác Sĩ

**Bảng an Lộc Tồn theo Thiên Can năm sinh:**
| Thiên Can | Lộc Tồn | Kình Dương | Đà La |
|-----------|---------|-----------|------|
| Giáp | Dần | Mão | Sửu |
| Ất | Mão | Thìn | Dần |
| Bính | Tị | Ngọ | Thìn |
| Đinh | Ngọ | Mùi | Tị |
| Mậu | Tị | Ngọ | Thìn |
| Kỷ | Ngọ | Mùi | Tị |
| Canh | Thân | Dậu | Mùi |
| Tân | Dậu | Tuất | Thân |
| Nhâm | Hợi | Tý | Tuất |
| Quý | Tý | Sửu | Hợi |

**Lưu ý:** Kình Dương = cung ngay sau Lộc Tồn; Đà La = cung ngay trước Lộc Tồn.

**Vòng Bác Sĩ (12 sao) - An từ vị trí Lộc Tồn:**
Bác Sĩ đặt cùng cung với Lộc Tồn (theo chiều thuận/nghịch phụ thuộc Âm Dương giới tính), rồi an lần lượt:

| STT | Tên Sao | Tính Chất |
|-----|---------|----------|
| 1 | Bác Sĩ | Thông minh, uyên bác, học vấn (Cát) |
| 2 | Lực Sĩ | Dũng cảm, sức mạnh, uy quyền (Cát) |
| 3 | Thanh Long | May mắn, tài lộc, hỷ sự (Cát) |
| 4 | Tiểu Hao | Hao tổn nhỏ, tiêu phí (Hung nhẹ) |
| 5 | Tướng Quân | Uy quyền, cứng rắn, võ lực (Cát/Hung) |
| 6 | Tấu Thư | Văn chương, truyền đạt, kiện tụng (Trung) |
| 7 | Phi Liêm | Phao tin, thị phi, tai họa (Hung) |
| 8 | Hỷ Thần | Vui vẻ, hỷ sự, tốt lành (Cát) |
| 9 | Bệnh Phù | Bệnh tật, yếu đuối, tang ma (Hung) |
| 10 | Đại Hao | Hao tổn lớn, tài chính thất bại (Hung) |
| 11 | Phục Binh | Phục kích, ẩn núp, bất ngờ (Hung) |
| 12 | Quan Phủ | Quan tụng, kiện cáo, pháp lý (Hung) |

**4 Nhóm tam hợp trong Vòng Bác Sĩ:**
- Nhóm 1: Bác Sĩ – Bệnh Phù – Tướng Quân
- Nhóm 2: Lực Sĩ – Đại Hao – Tấu Thư
- Nhóm 3: Thanh Long – Phục Binh – Phi Liêm
- Nhóm 4: Tiểu Hao – Quan Phủ – Hỷ Thần

### 3.3 Vòng Thái Tuế (12 sao)

**Cách an:** Thái Tuế đặt tại cung ứng với **địa chi của năm hiện tại** (lưu niên). Các sao còn lại an **thuận chiều** từ đó.

**Thứ tự 12 sao:**
| STT | Tên Sao | Tính Chất |
|-----|---------|----------|
| 1 | Thái Tuế | Uy quyền, chính trực, áp lực (Hung/Trung) |
| 2 | Thiếu Dương | Thông minh, cạnh tranh, sáng tạo (Cát) |
| 3 | Tang Môn | Tang tóc, buồn bã, mất mát (Hung) |
| 4 | Thiếu Âm | Khiêm nhường, tinh tế, nội tâm (Trung) |
| 5 | Quan Phù | Quan tụng, tranh chấp pháp lý (Hung) |
| 6 | Tử Phù | Phù trợ, giải quyết, hỗ trợ (Cát) |
| 7 | Tuế Phá | Phá hoại, đứt gãy, bất ngờ xấu (Hung) |
| 8 | Long Đức | Phúc đức, bình an, may mắn (Cát) |
| 9 | Bạch Hổ | Bạo lực, tai nạn, hung dữ (Hung) |
| 10 | Phúc Đức | Phúc báu, hỷ sự, hài lòng (Cát) |
| 11 | Điếu Khách | Tang lễ, chia ly, mất mát (Hung) |
| 12 | Trực Phù | Trực tiếp, chính trực, phụ trợ (Trung) |

**Lưu ý đặc biệt:** Khi an Thiếu Dương thì an Thiên Không cùng cung đó.

**4 Nhóm Tam Hợp của Vòng Thái Tuế:**
- Nhóm "Tuế Hổ Phù": Thái Tuế – Bạch Hổ – Quan Phù (bộc trực, chính trực)
- Nhóm "Tử Dương Phúc": Tử Phù – Thiếu Dương – Phúc Đức (thông minh, cạnh tranh)
- Nhóm "Phá Tang Điếu": Tuế Phá – Tang Môn – Điếu Khách (chống đối, mất mát)
- Nhóm "Long Âm Trực": Long Đức – Thiếu Âm – Trực Phù (khiêm nhường, ít tham vọng)

### 3.4 Các Phụ Tinh Quan Trọng Khác

#### Lục Phụ Trung Tinh (6 sao quan trọng nhất trong phụ tinh)
| Tên Sao | Cách An | Tính Chất |
|---------|---------|----------|
| Tả Phù | Theo tháng sinh | Phụ tá bên trái, hỗ trợ (Cát) |
| Hữu Bật | Theo tháng sinh | Phụ tá bên phải, hỗ trợ (Cát) |
| Văn Xương | Theo giờ sinh | Văn học, thi cử, học vấn (Cát) |
| Văn Khúc | Theo giờ sinh | Nghệ thuật, âm nhạc, tài năng (Cát) |
| Thiên Khôi | Theo Thiên Can | Quý nhân nam, cứu giúp (Cát) |
| Thiên Việt | Theo Thiên Can | Quý nhân nữ, cứu giúp (Cát) |

#### Bảng an Thiên Khôi và Thiên Việt theo Thiên Can:
| Thiên Can | Thiên Khôi | Thiên Việt |
|-----------|-----------|-----------|
| Giáp/Mậu | Sửu | Mùi |
| Ất/Kỷ | Tý | Thân |
| Bính/Đinh | Hợi | Dậu |
| Canh/Tân | Ngọ | Dần |
| Nhâm/Quý | Mão | Tị |

*(Lưu ý: Có 2 trường phái khác nhau về an Khôi Việt cho tuổi Canh-Tân)*

#### Tứ Sát Tinh (4 Sao Hung Mạnh Nhất)
| Tên Sao | Cách An | Tính Chất |
|---------|---------|----------|
| Hỏa Tinh | Theo giờ sinh + cục | Bạo lực, tàn nhẫn (Hung nặng) |
| Linh Tinh | Theo giờ sinh + cục | Âm mưu, ám hại (Hung nặng) |
| Địa Không | Theo giờ sinh | Hao tổn, trống rỗng (Hung) |
| Địa Kiếp | Theo giờ sinh | Cướp đoạt, mất mát (Hung) |

#### Các Phụ Tinh An Theo Địa Chi Năm Sinh
| Tên Sao | Ý Nghĩa |
|---------|---------|
| Thiên Mã | Di chuyển, xa quê, phát triển xa (Cát khi có Lộc Tồn) |
| Thiên Hỷ | Hỷ sự, đám cưới, tin vui |
| Thiên Quan | Quan lộc, chức tước |
| Thiên Phúc | Phúc lộc, giải trừ tai ách |
| Thiên Hình | Hình phạt, kỷ luật, y tế |
| Thiên Giải | Giải cứu, hóa giải điều xấu |
| Địa Giải | Giải hóa tai ách tại cõi đất |
| Giải Thần | Giải thần, hóa giải |

**Bảng an Thiên Mã theo Địa Chi năm sinh:**
- Dần, Ngọ, Tuất → Thiên Mã tại Thân
- Thân, Tý, Thìn → Thiên Mã tại Dần
- Tị, Dậu, Sửu → Thiên Mã tại Hợi
- Hợi, Mão, Mùi → Thiên Mã tại Tị

#### Phụ Tinh Bổ Sung Quan Trọng
| Tên Sao | Cách An | Tính Chất |
|---------|---------|----------|
| Lộc Tồn | Thiên Can năm | Tài lộc, phúc thọ, trường thọ |
| Kình Dương | Sau Lộc Tồn 1 cung | Sát tinh, cứng nhắc, hung dữ |
| Đà La | Trước Lộc Tồn 1 cung | Sát tinh, trì trệ, âm hiểm |
| Ân Quang | Theo năm | Ân huệ, ơn trên |
| Thiên Quý | Theo năm | Quý nhân phù trợ |
| Long Trì | Theo năm | Tài hoa, nghệ thuật |
| Phượng Các | Theo năm | Thanh danh, quý phái |
| Đào Hoa | Theo năm/giờ | Đào hoa, tình cảm, lãng mạn |
| Hồng Loan | Theo năm | Hôn nhân, tình duyên |
| Thiên Thọ | Theo năm | Trường thọ |
| Thiên Đức | Theo tháng | Đức hạnh, phúc lành |
| Nguyệt Đức | Theo tháng | Đức lành từ mặt trăng |
| Thai Phụ | Theo năm | Thai nghén, sinh sản |
| Phong Cáo | Theo năm | Thăng tiến, phong cấp |
| Quốc Ấn | Theo Thiên Can | Ấn quan, quyền lực nhà nước |
| Đường Phù | Theo Thiên Can | Hành chính, quan phủ |
| Tướng Quân | Trong vòng Bác Sĩ | Uy quyền quân sự |

---

## 4. HỆ THỐNG MIẾU VƯỢNG ĐẮC BÌNH HÃM

### Định Nghĩa 5 Cấp Độ
| Cấp | Ký Hiệu | Ý Nghĩa |
|-----|---------|---------|
| Miếu | M | Sáng nhất — Cát tinh rất tốt, Hung tinh giảm xấu rõ rệt |
| Vượng | V | Rất sáng — Cát tinh tốt mạnh, Hung tinh giảm hại |
| Đắc | Đ | Trung bình khá — Cát giữ tốt, Hung giảm nhẹ |
| Bình | B | Mờ — Cát còn chút tốt, Hung bắt đầu xấu |
| Hãm | H | Tối nhất — Cát mất ưu điểm, Hung khuếch đại xấu |

### Nguyên Tắc Quan Trọng
- **Cát tinh ở Hãm địa**: Mất tác dụng tốt, thậm chí sinh hại
- **Hung tinh ở Miếu địa**: Giảm tác dụng xấu, đôi khi phát huy mặt tốt tiềm ẩn
- **Ảnh hưởng hỗn hợp**: Khi cát tinh và hung tinh cùng cung → phân tích cân bằng

### Bảng Miếu Hãm Các Chính Tinh (Tóm Tắt)

| Sao | Miếu/Vượng Tại | Hãm Tại |
|-----|---------------|---------|
| Tử Vi | Tị, Ngọ, Dần, Thân | Hợi |
| Thiên Cơ | Mão, Thìn, Tị, Ngọ, Mùi | Dậu, Tuất, Hợi |
| Thái Dương | Dần → Ngọ (rạng dần), Mão, Thìn đỉnh | Tuất, Hợi, Tý (lặn) |
| Vũ Khúc | Thìn, Tuất, Sửu, Mùi, Dậu | Ngọ |
| Thiên Đồng | Tý, Dần, Thìn, Ngọ | Ngọ (một số phái), Mùi |
| Liêm Trinh | Dần, Ngọ, Tuất | Hợi, Tý, Sửu |
| Thiên Phủ | Dần, Ngọ, Tuất, Thìn, Sửu, Mùi | Ít khi hãm hoàn toàn |
| Thái Âm | Hợi, Tý, Sửu, Dậu | Ngọ, Tị (lúc giữa trưa) |
| Tham Lang | Dần, Mão, Tị, Ngọ | Thìn, Tuất, Sửu, Mùi |
| Cự Môn | Dần, Thân, Tị, Hợi | Ngọ, Tý |
| Thiên Tướng | Dần, Ngọ, Tuất | Thìn, Tuất, Sửu, Mùi |
| Thiên Lương | Ngọ, Dần, Thân | Tý, Sửu |
| Thất Sát | Thìn, Tuất, Sửu, Mùi, Dậu | Mão, Ngọ |
| Phá Quân | Thìn, Tuất, Sửu, Mùi, Tý | Ngọ, Dần, Thân |

*(Bảng đầy đủ chi tiết cần tra cứu thêm tại các tài liệu chuyên sâu)*

### Tại Sao Miếu Vượng Quan Trọng?
1. **Định mức độ ảnh hưởng**: Cùng một sao nhưng ở cung Miếu vs Hãm thì tác động hoàn toàn khác biệt
2. **Luận giải tổng thể**: Một lá số tốt/xấu phụ thuộc nhiều vào các sao chính có đắc địa không
3. **Điều chỉnh khi kết hợp**: Cát tinh ở Hãm + Hung tinh ở Miếu = rất phức tạp, cần phân tích kỹ

---

## 5. TỨ HÓA CHI TIẾT

### Định Nghĩa
Tứ Hóa là 4 loại biến chuyển khí hóa do **Thiên Can** tác động lên tinh diệu, thay đổi tính chất và năng lượng của sao đó theo hướng tốt hoặc xấu.

### Ý Nghĩa 4 Loại Hóa
| Hóa | Ý Nghĩa Chính | Biểu Tượng |
|-----|-------------|-----------|
| **Hóa Lộc** | Tài lộc, phú quý, may mắn, thịnh vượng | Mùa Xuân |
| **Hóa Quyền** | Quyền lực, kiên định, chấp trước, thăng tiến | Mùa Hạ |
| **Hóa Khoa** | Thanh danh, học vấn, quý nhân, tiếng tốt | Mùa Thu |
| **Hóa Kỵ** | Trở ngại, thị phi, ghen ghét, rủi ro | Mùa Đông |

### Bảng Tứ Hóa Theo 10 Thiên Can (Trường Phái Nam Phái)
| Thiên Can | Hóa Lộc | Hóa Quyền | Hóa Khoa | Hóa Kỵ |
|-----------|---------|----------|---------|--------|
| **Giáp** | Liêm Trinh | Phá Quân | Vũ Khúc | Thái Dương |
| **Ất** | Thiên Cơ | Thiên Lương | Tử Vi | Thái Âm |
| **Bính** | Thiên Đồng | Thiên Cơ | Văn Xương | Liêm Trinh |
| **Đinh** | Thái Âm | Thiên Đồng | Thiên Cơ | Cự Môn |
| **Mậu** | Tham Lang | Thái Âm | Hữu Bật | Thiên Cơ |
| **Kỷ** | Vũ Khúc | Tham Lang | Thiên Lương | Văn Khúc |
| **Canh** | Thái Dương | Vũ Khúc | Thái Âm | Thiên Đồng |
| **Tân** | Cự Môn | Thái Dương | Văn Khúc | Văn Xương |
| **Nhâm** | Thiên Lương | Tử Vi | Tả Phù | Vũ Khúc |
| **Quý** | Phá Quân | Cự Môn | Thái Âm | Tham Lang |

### Phi Hóa (Flying Transformation) là gì?
Phi Hóa = áp dụng Tứ Hóa của **Thiên Can từng cung** (không phải chỉ Thiên Can năm sinh) để xem ảnh hưởng lan sang các cung khác.

**Ví dụ:** Nếu cung Mệnh có Thiên Can Nhâm:
- Lấy bảng Tứ Hóa của Nhâm: Lộc→Thiên Lương, Quyền→Tử Vi, Khoa→Tả Phù, Kỵ→Vũ Khúc
- Các biến hóa này "phi" vào các cung chứa sao tương ứng
- Tạo thêm một lớp phân tích sâu hơn về tương tác giữa các cung

**Tiên Thiên Tứ Hóa:** Dựa trên Thiên Can năm sinh (cố định suốt đời)
**Hậu Thiên Tứ Hóa / Phi Hóa:** Dựa trên Thiên Can từng cung (biến động theo cung)

---

## 6. CAN CHI TỪNG CUNG

### Địa Chi Các Cung (Cố Định Trên Thiên Bàn)
Thiên bàn Tử Vi có 12 cung ứng với 12 địa chi cố định theo vị trí:
- Cung Tý (vị trí 1), Sửu (2), Dần (3), Mão (4), Thìn (5), Tị (6)
- Ngọ (7), Mùi (8), Thân (9), Dậu (10), Tuất (11), Hợi (12)

### Cách Xác Định Cung Mệnh
Cung Mệnh được xác định dựa trên:
1. **Tháng sinh âm lịch** → xác định hàng ngang (dòng tháng)
2. **Giờ sinh âm lịch** (12 giờ địa chi) → xác định cung Mệnh

Bảng tra: Tháng sinh × Giờ sinh → Cung Mệnh (địa chi của cung Mệnh)

### Thiên Can Của Từng Cung
Sau khi xác định cung Mệnh (biết địa chi), các cung còn lại được đặt theo chiều thuận.

**Thiên Can các cung được tính từ Thiên Can năm sinh:**
- Dùng Thiên Can năm sinh làm cơ sở
- Áp dụng quy tắc "Ngũ Hổ Độn Niên" để tìm Thiên Can của cung Dần (tháng 1)
- Từ đó suy ra Thiên Can tháng 2, 3,... (mỗi tháng tiếp = Can tiếp theo)

**Bảng Ngũ Hổ Độn (Thiên Can Tháng theo Thiên Can Năm):**
| Thiên Can Năm | Can Cung Dần (Tháng 1) |
|--------------|----------------------|
| Giáp / Kỷ | Bính |
| Ất / Canh | Mậu |
| Bính / Tân | Canh |
| Đinh / Nhâm | Nhâm |
| Mậu / Quý | Giáp |

Từ Can tháng Dần, đếm thuận theo 10 Can: Dần, Mão, Thìn, Tị, Ngọ, Mùi, Thân, Dậu, Tuất, Hợi, Tý, Sửu.

---

## 7. MỆNH CHỦ VÀ THÂN CHỦ

### Mệnh Chủ
Mệnh Chủ được xác định theo **Địa Chi của Cung Mệnh** (tức là địa chi của cung Mệnh trong lá số).

**7 sao Bắc Đẩu làm Mệnh Chủ (theo thứ tự 12 địa chi):**
| Địa Chi Cung Mệnh | Mệnh Chủ |
|-----------------|---------|
| Tý | Tham Lang |
| Sửu | Cự Môn |
| Dần | Lộc Tồn |
| Mão | Văn Khúc |
| Thìn | Liêm Trinh |
| Tị | Vũ Khúc |
| Ngọ | Phá Quân |
| Mùi | Tham Lang |
| Thân | Cự Môn |
| Dậu | Lộc Tồn |
| Tuất | Văn Khúc |
| Hợi | Liêm Trinh |

*(Chu kỳ 7 sao lặp lại)*

### Thân Chủ
Thân Chủ được xác định theo **Địa Chi của Năm Sinh** (tuổi âm lịch).

**6 sao làm Thân Chủ (theo thứ tự 12 địa chi năm sinh):**
| Địa Chi Năm Sinh | Thân Chủ |
|----------------|---------|
| Tý | Linh Tinh |
| Sửu | Thiên Tướng |
| Dần | Thiên Lương |
| Mão | Thiên Đồng |
| Thìn | Văn Xương |
| Tị | Thiên Cơ |
| Ngọ | Hỏa Tinh |
| Mùi | Thiên Tướng |
| Thân | Thiên Lương |
| Dậu | Thiên Đồng |
| Tuất | Văn Xương |
| Hợi | Thiên Cơ |

*(Chu kỳ 6 sao lặp lại)*

### Vai Trò Trong Luận Giải
- **Mệnh Chủ**: Phản ánh tính cách, cá tính, hành vi cơ bản
- **Thân Chủ**: Phản ánh thân thể, vận mệnh tổng thể, điều kiện cuộc đời
- Khi Mệnh Chủ hoặc Thân Chủ gặp Hóa Kỵ, Hung Tinh → ảnh hưởng rất nặng nề

---

## 8. ĐẠI HẠN, TIỂU HẠN, LƯU NIÊN

### 8.1 Đại Hạn (Vận 10 Năm)

**Khái niệm:** Mỗi đại hạn kéo dài **10 năm**, chiếm một cung trong lá số.

**Cách tính tuổi bắt đầu đại hạn thứ nhất:**
Dựa vào **Ngũ Hành Cục**:
- Thủy Nhị Cục → Đại hạn 1 bắt đầu năm **2 tuổi**
- Mộc Tam Cục → Đại hạn 1 bắt đầu năm **3 tuổi**
- Kim Tứ Cục → Đại hạn 1 bắt đầu năm **4 tuổi**
- Thổ Ngũ Cục → Đại hạn 1 bắt đầu năm **5 tuổi**
- Hỏa Lục Cục → Đại hạn 1 bắt đầu năm **6 tuổi**

**Chiều di chuyển đại hạn:**
- Dương Nam + Âm Nữ → Đại hạn đi **thuận chiều** (từ cung Mệnh sang Huynh Đệ, Thê Thiếp...)
- Âm Nam + Dương Nữ → Đại hạn đi **nghịch chiều** (từ cung Mệnh sang Phụ Mẫu, Phúc Đức...)

**Ví dụ (Dương Nam, Thủy Nhị Cục):**
- 2-11 tuổi: Cung Mệnh
- 12-21 tuổi: Cung Huynh Đệ
- 22-31 tuổi: Cung Thê Thiếp
- 32-41 tuổi: Cung Tử Tức
- 42-51 tuổi: Cung Tài Bạch
- 52-61 tuổi: Cung Tật Ách
- ... (tiếp tục 12 cung)

### 8.2 Tiểu Hạn (Vận 1 Năm)

**Khái niệm:** Mỗi tiểu hạn kéo dài **1 năm**, chiếm một cung.

**Cách tính cung Tiểu Hạn năm 1 tuổi:**
Dựa vào **tam hợp năm sinh**:
- Dần, Ngọ, Tuất (Hỏa) → Tiểu hạn năm 1 tại cung **Thìn**
- Thân, Tý, Thìn (Thủy) → Tiểu hạn năm 1 tại cung **Tuất**
- Tị, Dậu, Sửu (Kim) → Tiểu hạn năm 1 tại cung **Mùi**
- Hợi, Mão, Mùi (Mộc) → Tiểu hạn năm 1 tại cung **Sửu**

**Chiều di chuyển Tiểu Hạn:**
- Nam → Tiểu hạn đi **thuận chiều**
- Nữ → Tiểu hạn đi **nghịch chiều**
- Mỗi năm chiếm 1 cung, 12 năm quay về vị trí cũ

### 8.3 Lưu Niên (Vận Hàng Năm)

**Lưu Niên** = Xem ảnh hưởng của năm hiện tại đối với toàn bộ lá số.
Cách xem:
1. Vòng Thái Tuế đặt theo địa chi năm hiện tại
2. Lưu Lộc, Lưu Mã, Lưu Hóa đặt theo Thiên Can năm hiện tại
3. Phân tích tương tác của các lưu tinh với cung đại hạn, tiểu hạn

**Lưu Đại Vận:** Hướng di chuyển của đại hạn trong năm đó, xác định vận hướng chính xác hơn. Lưu đại vận là "hướng thực" của đại hạn cho từng năm cụ thể.

---

## 9. TUẦN VÀ TRIỆT

### Khái Niệm
- **Tuần Không** (Tuần): Trói buộc, kìm hãm, ngăn chặn nhẹ
- **Triệt Không** (Triệt): Cắt bỏ, đứt gãy, chia cắt mạnh hơn

### Cách An
- Tuần Không và Triệt Không được xác định theo **Năm Sinh** (can chi năm)
- Đặc biệt: Chúng **không tọa thủ trong một cung** mà nằm giữa **ranh giới 2 cung**
- Cung bị Tuần/Triệt chiếu vào sẽ bị ảnh hưởng

### Ảnh Hưởng
- Làm **giảm** tác động của cả cát tinh lẫn hung tinh trong cung đó
- Không làm biến đổi **bản chất** của sao (không thể biến hung thành cát)
- Cát tinh bị Tuần/Triệt → giảm tốt
- Hung tinh bị Tuần/Triệt → giảm bớt xấu (nhưng cũng giảm cả tốt)

### Quan Điểm Trường Phái
- Có nhiều tranh luận về nguồn gốc và cách áp dụng Tuần Triệt
- Trường phái Tam Hợp coi Tuần Triệt là công cụ **phụ trợ**, không phải yếu tố chính
- Trường phái Tứ Hóa ít chú trọng Tuần Triệt hơn
- HOROS (app hiện đại) gợi ý dùng làm "công cụ phân tích bổ sung"

---

## 10. HỆ THỐNG ĐIỂM CUNG

### Tổng Quan
Một số app tử vi hiện đại tính **điểm** (score) cho mỗi cung để người dùng dễ so sánh các lĩnh vực trong cuộc sống.

### Mô Hình Tính Điểm (Tổng Hợp Từ Các App)

**Nguyên tắc chung:**
1. Mỗi sao trong cung đóng góp điểm (+/-)
2. Cát tinh = điểm dương; Hung tinh = điểm âm
3. Mức độ Miếu/Vượng/Đắc/Bình/Hãm nhân hệ số
4. Tứ Hóa ảnh hưởng mạnh: Hóa Lộc (+), Hóa Quyền (+), Hóa Khoa (+), Hóa Kỵ (-)

**Các yếu tố ảnh hưởng điểm:**
| Yếu Tố | Tác Động |
|--------|---------|
| Chính tinh Miếu/Vượng | Tăng điểm mạnh |
| Chính tinh Hãm | Giảm điểm |
| Hóa Lộc/Quyền/Khoa | Tăng điểm |
| Hóa Kỵ | Giảm điểm nặng |
| Cát tinh hội tụ (Tả Phù, Hữu Bật, Thiên Khôi, Thiên Việt...) | Tăng điểm |
| Tứ Sát (Kình, Đà, Hỏa, Linh, Không, Kiếp) | Giảm điểm |
| Trường Sinh, Đế Vượng (Vòng Tràng Sinh) | Điểm tốt |
| Mộ, Tuyệt, Tử (Vòng Tràng Sinh) | Điểm xấu |

### TuviData (BigData Scoring)
- Chấm điểm **chính xác đến từng phút sinh**
- Tổng hợp từ **hàng nghìn lá số** thực tế
- Cung cấp điểm số cho: Sự nghiệp, Tài chính, Tình cảm, Sức khỏe, Vận 12 năm
- Có hệ thống điều chỉnh theo phút sinh khác nhau

### TinhMenhDo
- Dùng **thuật toán thiên văn tiên tiến** để quy đổi và tinh chỉnh lá số
- Tích hợp AI để luận đoán
- Hiển thị đầy đủ 14 chính tinh + phụ tinh + vòng sao
- Có tính năng xem Đại Hạn chi tiết

---

## 11. SO SÁNH CÁC APP TỬ VI NỔI TIẾNG

### TinhMenhDo (tinhmenhdo.com)
**Điểm mạnh:**
- Lá số đầy đủ nhất theo đánh giá người dùng Việt
- Hỗ trợ cả Nam Phái và Việt Nam Phái
- Có AI luận đoán tổng quan
- Thuật toán thiên văn tiên tiến
- Hiển thị: 14 chính tinh, đầy đủ phụ tinh, vòng sao, Tứ Hóa, Đại Hạn, Tiểu Hạn

**Tính năng hiển thị lá số:**
- Bố cục 12 ô cung dạng bảng truyền thống
- Hiển thị Can Chi từng cung
- Màu sắc phân biệt cát/hung
- Điểm đánh giá từng cung (theo AI)

### TuviData (tuvidata.com)
**Điểm mạnh:**
- Hệ thống chấm điểm BigData độc đáo
- Chính xác đến phút sinh
- Báo cáo phân tích chi tiết theo từng lĩnh vực
- Cung cấp vận 12 năm

**Dịch vụ:**
- Miễn phí: An sao cơ bản
- Có phí (229k-259k VND): Báo cáo đầy đủ

### HOROS (horos.vn)
**Điểm mạnh:**
- Giao diện hiện đại, phù hợp thế hệ mới
- Nội dung giáo dục phong phú (blog, bài viết)
- Cách tiếp cận học thuật, minh bạch về phương pháp
- Phân tích Tứ Hóa, Phi Hóa sâu

**Định vị:** "Tử Vi cho thế hệ mới" - kết hợp truyền thống và hiện đại

### TracuuTuVi (tracuutuvi.com)
**Điểm mạnh:**
- Thông tin chi tiết về từng sao
- Tra cứu nhanh
- Nhiều bài viết giải thích từng khái niệm

### Lịch Vạn Niên (lichngaytot.com)
**Điểm mạnh:**
- Tích hợp với Lịch Âm, Lịch Dương
- Tra cứu nhanh thông tin ngày tháng
- Phần Tử Vi là tính năng bổ sung
- Phù hợp người dùng phổ thông

### AITUVI (aituvi.com)
**Điểm mạnh:**
- Tích hợp AI để luận giải
- Chính xác cao theo quảng cáo
- Giao diện thân thiện

---

## 12. NGUỒN THAM KHẢO

- [Các Sao Trong Tử Vi - Tổng Quan](https://thansohoconline.com/cac-sao-trong-tu-vi.html)
- [Các Sao Trong Tử Vi - TracuuTuVi](https://tracuutuvi.com/cac-sao-trong-tu-vi.html)
- [Các Sao Phụ Quan Trọng - HOROS](https://horos.vn/blog/post/cac-sao-phu-quan-trong-trong-mon-tu-vi)
- [Vòng Tràng Sinh - TracuuLaSoTuVi](https://tracuulasotuvi.com/vong-trang-sinh.html)
- [Vòng Tràng Sinh - TuviVN](https://tuvi.vn/vong-trang-sinh-la-gi-a681)
- [Vòng Thái Tuế - Thanso](https://thansohoconline.com/vong-thai-tue.html)
- [Vòng Thái Tuế, Tràng Sinh, Lộc Tồn - TuviVietNam](https://tuvivietnam.vn/vong-thai-tue-vong-trang-sinh-vong-loc-ton/)
- [Cách An Lộc Tồn, Kình Dương, Đà La - HocVienLySo](https://hocvienlyso.org/cach-an-vong-loc-ton-kinh-duong-da-la-thien-khoi-thien-viet.html)
- [Bảng Tứ Hóa Theo Thiên Can - GiaiThan](http://giaithan.vn/bang-tu-hoa-theo-thien-can/)
- [Tứ Hóa Trong Tử Vi - TracuuTuVi](https://tracuutuvi.com/tu-hoa.html)
- [Tứ Hóa và Phi Hóa - HocVienLySo](https://hocvienlyso.org/chuong-14-tu-hoa-va-phi-hoa.html)
- [Miếu Vượng Đắc Bình Hãm - HOROS](https://horos.vn/blog/post/mieu-vuong-dac-binh-ham-la-gi-phan-biet-do-sang-cac-sao-trong-tu-vi)
- [Miếu Hãm Các Tinh Diệu - SonChu](https://sonchu.vn/2022/08/15/chuong-21-thuyet-mieu-ham-cua-cac-tinh-dieu/)
- [Tuần và Triệt - HOROS](https://horos.vn/blog/post/nhung-dieu-co-the-ban-chua-biet-ve-tuan-va-triet)
- [Tuần Triệt - TracuuTuVi](https://tracuutuvi.com/tuan-triet.html)
- [Mệnh Chủ và Thân Chủ - TuviCohoc](https://tuvi.cohoc.net/menh-chu-va-than-chu-nid-164.html)
- [Cách Tính Vận Hạn - TracuuLaSoTuVi](https://tracuulasotuvi.com/cach-tinh-van-han-trong-tu-vi.html)
- [Đại Tiểu Hạn - TuviCohoc](https://tuvi.cohoc.net/xet-ve-dai-tieu-han-nhung-cach-tinh-dai-han-dai-han-luu-nien-la-gi-va-cac-luu-tinh-la-gi-nid-122.html)
- [Sao Bác Sĩ - TracuuTuVi](https://tracuutuvi.com/sao-bac-si.html)
- [Vòng Bác Sĩ Và Lộc Tồn - NgocBinh](https://ngocbinh1974.violet.vn/entry/phan-viii-phuong-phap-an-vong-loc-ton-bac-sy-va-cac-sao-co-cung-dac-tinh-voi-vong-loc-ton-bac-sy-8891058.html)
- [TinhMenhDo - Lá Số Đầy Đủ](https://tinhmenhdo.com/tu-vi/la-so-tu-vi-viet-nam/)
- [TuviData - BigData Scoring](https://tuvidata.com/)
- [HOROS - Tứ Hóa](https://horos.vn/blog/post/tu-hoa-la-gi-phan-biet-4-sao-hoa-trong-tu-vi)

---

## PHỤ LỤC: CHECKLIST TRIỂN KHAI KỸ THUẬT

### Các Bảng Tra Cần Hardcode Trong App

- [ ] Bảng an Tử Vi + 13 chính tinh theo Cục + Ngày sinh
- [ ] Bảng Tứ Hóa (10 Can × 4 loại hóa)
- [ ] Bảng Lộc Tồn + Kình Dương + Đà La (10 Can)
- [ ] Bảng Thiên Khôi + Thiên Việt (10 Can)
- [ ] Bảng Vòng Tràng Sinh khởi điểm theo Cục
- [ ] Bảng Mệnh Chủ theo 12 Địa Chi cung Mệnh
- [ ] Bảng Thân Chủ theo 12 Địa Chi năm sinh
- [ ] Bảng Thiên Mã theo tam hợp Địa Chi năm
- [ ] Bảng Tuần + Triệt theo Can Chi năm
- [ ] Bảng Miếu Vượng Đắc Bình Hãm (14 sao × 12 cung)
- [ ] Bảng an Tiểu Hạn theo tam hợp năm sinh
- [ ] Bảng Ngũ Hổ Độn (Thiên Can tháng theo Thiên Can năm)
- [ ] Bảng an Văn Xương + Văn Khúc theo giờ sinh
- [ ] Bảng an Hỏa Tinh + Linh Tinh theo giờ + cục
- [ ] Bảng an Địa Không + Địa Kiếp theo giờ sinh

### Thứ Tự An Sao Đề Xuất
1. Xác định Cung Mệnh (tháng × giờ)
2. Xác định Ngũ Hành Cục (can chi năm + cung Mệnh)
3. An 14 Chính Tinh
4. An Tứ Hóa (theo Can năm)
5. An Vòng Tràng Sinh (theo Cục + Âm Dương)
6. An Vòng Lộc Tồn + Bác Sĩ (theo Can năm)
7. An Vòng Thái Tuế (theo Địa Chi năm hiện tại)
8. An các Phụ Tinh còn lại (Thiên Khôi/Việt, Văn Xương/Khúc, Tứ Sát...)
9. An Mệnh Chủ + Thân Chủ
10. Xác định Tuần Triệt
11. Tính Đại Hạn + Tiểu Hạn hiện tại
