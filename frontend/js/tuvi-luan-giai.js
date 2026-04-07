/**
 * Tử Vi — Luận Giải Lá Số v1
 * Tra cứu ý nghĩa sao theo cung, sinh văn luận giải tự động.
 */

// =========================================
// DATABASE — Chính Tinh × Cung
// =========================================
const LG_CHINH_TINH = {
    'Tử Vi': {
        'Mệnh':     'Tử Vi thủ Mệnh: Người có tướng mạo đoan chính, khí độ bề trên, có chí lớn, ưa quyền lực và được mọi người kính trọng. Có năng lực lãnh đạo, cầu toàn, tự trọng cao.',
        'Phu Thê':  'Tử Vi cư Phu Thê: Lấy được vợ/chồng con nhà danh giá, gia đình hôn phối nhiều người có địa vị. Vợ chồng bảo ban nhau trong làm ăn và nuôi dạy con cái.',
        'Quan Lộc': 'Tử Vi cư Quan Lộc: Có năng lực lãnh đạo xuất sắc, dễ đạt được chức vụ cao. Công việc mang tính quyền lực, quản lý, điều hành.',
        'Tử Tức':   'Tử Vi cư Tử Tức: Con cái thông minh, có chí, dễ thành danh. Con cái ngoan ngoãn, hiếu thảo.',
        '_':        'Tử Vi đóng cung này: Mang lại quyền uy, sự cao sang, bảo hộ. Cung được chiếu sáng bởi đế tinh — tốt lành và uy phong.',
    },
    'Thiên Cơ': {
        'Mệnh':     'Thiên Cơ thủ Mệnh: Người thông minh, linh hoạt, nhiều mưu kế. Thích suy tư, hay thay đổi, giỏi tính toán. Phù hợp ngành tư vấn, nghiên cứu, kế hoạch.',
        'Quan Lộc': 'Thiên Cơ cư Quan Lộc: Công việc đòi hỏi tư duy sáng tạo, mưu lược. Dễ thay đổi nghề, hợp làm tư vấn, chiến lược, IT, thiết kế.',
        'Phụ Mẫu':  'Thiên Cơ cư Phụ Mẫu: Cha mẹ thông minh, linh hoạt, hay thay đổi. Được cha mẹ truyền tư duy nhạy bén.',
        'Nô Bộc':   'Thiên Cơ cư Nô Bộc: Bạn bè thông minh, mưu lược nhưng hay thay đổi. Quan hệ phức tạp, cần cẩn thận trong giao đãi.',
        '_':        'Thiên Cơ đóng cung này: Mang tính linh hoạt, biến chuyển, tư duy. Cần cẩn thận với sự thay đổi không ổn định.',
    },
    'Thái Dương': {
        'Mệnh':     'Thái Dương thủ Mệnh: Người phóng khoáng, nhiệt tình, năng động. Nam mệnh Nhật hào quý, dễ nổi danh. Hợp làm lãnh đạo, ngoại giao, chính trị.',
        'Quan Lộc': 'Thái Dương cư Quan Lộc: Công danh sự nghiệp rực rỡ. Phù hợp công tác quản lý, chính quyền, ngoại giao, truyền thông.',
        'Tài Bạch':  'Thái Dương cư Tài Bạch: Kiếm tiền từ các hoạt động công khai, đông người, hoặc có liên quan nước ngoài. Thu nhập ổn định từ sự nghiệp.',
        'Tật Ách':  'Thái Dương cư Tật Ách: Dễ mắc bệnh về mắt, đau đầu, căng thẳng thần kinh.',
        '_':        'Thái Dương đóng cung này: Mang ánh sáng, uy danh, sự công khai. Tốt cho việc mở rộng quan hệ và danh tiếng.',
    },
    'Vũ Khúc': {
        'Mệnh':     'Vũ Khúc thủ Mệnh: Người cứng rắn, quyết đoán, cô độc, giỏi tài chính. Ít nói nhưng làm được việc lớn. Phù hợp kinh doanh, tài chính, quân sự.',
        'Quan Lộc': 'Vũ Khúc cư Quan Lộc: Công việc liên quan tài chính, ngân hàng, kinh doanh, hoặc các ngành đòi hỏi sự chính xác. Một mình lập nghiệp.',
        'Thiên Di':  'Vũ Khúc cư Thiên Di: Ít đi ra ngoài, thích làm việc một mình, ngại đến nơi mới. Khi đi là vì công việc hoặc gia đình.',
        'Tài Bạch':  'Vũ Khúc cư Tài Bạch: Kiếm tiền rất giỏi, chắt chiu, tài chính vững. Tiền tự đến tay — đặc biệt tốt khi về già.',
        '_':        'Vũ Khúc đóng cung này: Mang lại sự chắc chắn, tiền bạc, nghị lực. Cần chú ý tránh cô lập quá mức.',
    },
    'Thiên Đồng': {
        'Mệnh':     'Thiên Đồng thủ Mệnh: Người ôn hoà, phúc hậu, được yêu thích. Hưởng thụ cuộc sống, ít tranh đấu. Phù hợp ngành phúc lợi, giáo dục, nghệ thuật.',
        'Quan Lộc': 'Thiên Đồng cư Quan Lộc: Công việc nhẹ nhàng, được đồng nghiệp yêu mến. Dễ thành công nhờ phúc phần hơn là tranh đấu.',
        'Nô Bộc':   'Thiên Đồng cư Nô Bộc: Bạn bè nhiều thành phần nhưng vui vẻ. Có bạn bè ham vui, ham chơi.',
        '_':        'Thiên Đồng đóng cung này: Mang lại phúc lành, hoà thuận, nhẹ nhàng. Hoá cát trừ hung tốt.',
    },
    'Liêm Trinh': {
        'Mệnh':     'Liêm Trinh thủ Mệnh: Người nghiêm nghị, đa tài nhưng đa sầu. Cương trực, có chính kiến, dễ vướng pháp lý nếu không cẩn thận.',
        'Tài Bạch':  'Liêm Trinh cư Tài Bạch: Chi tiêu tiền rất mạnh, dễ đam mê cờ bạc, thú vui tầm thường. Khéo tiêu nhưng khó giữ tiền.',
        'Phúc Đức': 'Liêm Trinh cư Phúc Đức: Tổ tiên từng gặp nạn oan. Cuộc đời phải vất vả đấu tranh, họ tộc ít đoàn kết.',
        '_':        'Liêm Trinh đóng cung này: Hóa khí là Tù Tinh — cẩn thận pháp luật, áp lực, ràng buộc. Cần chính trực mới hoá tốt.',
    },
    'Thiên Phủ': {
        'Mệnh':     'Thiên Phủ thủ Mệnh: Người mặt tròn da trắng, ôn hoà, thông minh tài ba. Giỏi kiếm tiền, chi tiêu phóng khoáng. Luôn là trung tâm quản lý tiền bạc, kho tàng. Ăn ngon mặc đẹp, gọn gàng sạch sẽ.',
        'Quan Lộc': 'Thiên Phủ cư Quan Lộc: Quản lý tốt, công việc ổn định, tiền lương đều đặn. Cai quản về kho bãi, tài sản tổ chức.',
        'Tài Bạch':  'Thiên Phủ cư Tài Bạch: Tiền bạc dồi dào, giỏi quản lý tài chính. Đi đâu cũng được giữ tiền cầm tiền.',
        '_':        'Thiên Phủ đóng cung này: Mang lại sự phồn thịnh, vật chất, ổn định. Tốt lành ở bất kỳ cung nào.',
    },
    'Thái Âm': {
        'Mệnh':     'Thái Âm thủ Mệnh: Người dịu dàng, khéo léo, giàu tình cảm. Nữ mệnh Thái Âm rất đẹp. Liên quan tài chính, bất động sản.',
        'Phụ Mẫu':  'Thái Âm cư Phụ Mẫu: Cha mẹ giàu có, khéo léo. Gần gũi mẹ hơn. Được mẹ nâng đỡ, có tài sản thừa kế.',
        'Tài Bạch':  'Thái Âm cư Tài Bạch: Tiền bạc đến từ đầu tư, bất động sản, tài chính. Tích luỹ tốt, nhất là về đêm hoặc nghề liên quan phụ nữ.',
        '_':        'Thái Âm đóng cung này: Khí phú chủ tài. Mang lại sự dịu dàng, tài chính, âm phúc.',
    },
    'Tham Lang': {
        'Mệnh':     'Tham Lang thủ Mệnh: Người đa tài, đa dục, thích hưởng thụ. Biến hoá linh hoạt, giỏi giao tiếp, hấp dẫn. Dễ sa vào ăn chơi nếu không kiểm soát.',
        'Tài Bạch':  'Tham Lang cư Tài Bạch: Nếu Đắc thì kiếm tiền nhanh, phát lộc. Nếu Hãm thì tiền tụ tán, khó giữ. Hợp buôn bán, kinh doanh.',
        'Phúc Đức': 'Tham Lang cư Phúc Đức: Tổ tiên có nhiều công lao, con cháu ngày sau nhiều người có tiếng tăm.',
        '_':        'Tham Lang đóng cung này: Đa dục, biến hoá, ham vui. Cần kiểm soát bản thân.',
    },
    'Cự Môn': {
        'Mệnh':     'Cự Môn thủ Mệnh: Người ăn nói hùng hồn nhưng hay gây thị phi. Tài về ngôn luận, sư phạm, luật. Cần cẩn thận miệng lưỡi.',
        'Điền Trạch': 'Cự Môn cư Điền Trạch: Nhà cao cửa rộng nhưng gần nơi ồn ào (chợ, karaoke). Dễ tranh chấp nhà đất, pháp lý.',
        'Nô Bộc':   'Cự Môn cư Nô Bộc: Bạn bè hay cãi vã, thị phi. Cần kiểm soát lời nói trong giao tiếp.',
        '_':        'Cự Môn đóng cung này: Hay sinh thị phi, tranh chấp. Dùng tốt thì giỏi hùng biện, tư vấn.',
    },
    'Thiên Tướng': {
        'Mệnh':     'Thiên Tướng thủ Mệnh: Người công bằng, nghiêm nghị, thích giúp đỡ. Cả đời hy sinh cho người khác. Phù hợp pháp luật, hành chính, quản lý.',
        'Quan Lộc': 'Thiên Tướng cư Quan Lộc: Làm lãnh đạo, quản lý, hy sinh cho công việc. Hợp làm luật, nghiên cứu, giảng dạy, tư vấn, tâm linh.',
        '_':        'Thiên Tướng đóng cung này: Mang lại sự công bằng, hỗ trợ, quản lý. Tốt cho công việc và quan hệ.',
    },
    'Thiên Lương': {
        'Mệnh':     'Thiên Lương thủ Mệnh: Người nhân từ, thọ, hay giúp đỡ người khác. Tính thiện lương, hướng đến học thuật, y tế, tâm linh.',
        'Quan Lộc': 'Thiên Lương cư Quan Lộc: Làm thầy, làm thầy thuốc, nhà nghiên cứu, hoặc cố vấn. Công việc thiên về trí tuệ và phục vụ.',
        'Nô Bộc':   'Thiên Lương cư Nô Bộc: Bạn bè hiền lành, nhân hậu. Nhiều bạn làm thầy giáo, thầy thuốc.',
        '_':        'Thiên Lương đóng cung này: Sao thiện ấm, ôn hoà, trường thọ. Giải trừ ách nạn tốt.',
    },
    'Thất Sát': {
        'Mệnh':     'Thất Sát thủ Mệnh: Người cá tính mạnh, quyết đoán, hay đấu tranh. Dễ bị tai nạn nếu không cẩn thận. Phù hợp quân sự, võ thuật, kinh doanh mạo hiểm.',
        'Quan Lộc': 'Thất Sát cư Quan Lộc: Công việc đòi hỏi đấu tranh, cạnh tranh. Dễ lên nhanh nhưng cũng dễ xuống. Phù hợp ngành có tính chiến đấu.',
        'Thiên Di':  'Thất Sát cư Thiên Di: Ra ngoài phải đấu tranh, dễ bị hình thương. Cẩn thận tai nạn khi di chuyển.',
        '_':        'Thất Sát đóng cung này: Mang tính chiến đấu, biến động, rủi ro. Cần dũng cảm nhưng cũng cần thận trọng.',
    },
    'Phá Quân': {
        'Mệnh':     'Phá Quân thủ Mệnh: Người phá cách, cải cách, ưa thay đổi. Dám phá bỏ cái cũ để xây dựng cái mới. Cuộc đời nhiều biến động.',
        'Phu Thê':  'Phá Quân cư Phu Thê: Vợ chồng dễ cách trở, làm ăn hao hụt. Một số trường hợp làm trong lực lượng vũ trang.',
        '_':        'Phá Quân đóng cung này: Phá cũ lập mới, biến động mạnh. Cần dùng đúng chỗ mới phát huy được.',
    },
};

// =========================================
// DATABASE — Phụ Tinh & Tạp Tinh × Cung
// =========================================
const LG_PHU_TINH = {
    // Tứ Hóa
    'Hóa Lộc':   { '_': 'Hóa Lộc tại đây: Tài lộc hanh thông, may mắn về tiền bạc, vật chất dồi dào. Vợ/chồng chăm chút chiều chuộng nhau (nếu tại Phu Thê).' },
    'Hóa Quyền': { '_': 'Hóa Quyền tại đây: Quyền lực, uy thế, chủ động trong công việc và cuộc sống.' },
    'Hóa Khoa':  {
        'Phụ Mẫu': 'Hóa Khoa tại Phụ Mẫu: Cha mẹ danh giá, kiến thức rộng. Được lớn lên trong môi trường học thức, tiếp thu nhiều thói quen tốt từ cha mẹ.',
        'Thiên Di': 'Hóa Khoa tại Thiên Di: Cát lợi cho học hành thi cử ở xa, công tác nước ngoài. Giải ách trừ tai khi xuất ngoại.',
        '_': 'Hóa Khoa tại đây: Danh tiếng, học vấn, thi cử thuận lợi. Giải trừ tai ách.',
    },
    'Hóa Kỵ':   {
        'Phúc Đức': 'Hóa Kỵ tại Phúc Đức: Họ hàng dễ lục đục, tranh giành. Nghiệp ảnh hưởng lên suy nghĩ và hôn nhân.',
        'Tật Ách':  'Hóa Kỵ tại Tật Ách: Bệnh tật phát ra trong năm khó tránh. Sức khoẻ đột ngột đi xuống, cần chú ý nội tạng.',
        '_': 'Hóa Kỵ tại đây: Kỵ thần — cản trở, ách nạn. Cần cẩn thận ở lĩnh vực liên quan đến cung này.',
    },

    // Văn Xương / Văn Khúc
    'Văn Xương': {
        'Mệnh':     'Văn Xương tại Mệnh: Tài hoa văn chương, học giỏi, thi cử thuận lợi. Tướng thư sinh, nhã nhặn.',
        'Quan Lộc': 'Văn Xương tại Quan Lộc: Công việc học thuật, nghiên cứu, giảng dạy. Dễ có học hàm học vị. Cả đời đam mê học hành.',
        '_': 'Văn Xương tại đây: Tài hoa, văn chương, học vấn. Tốt cho thi cử và danh tiếng học thuật.',
    },
    'Văn Khúc': {
        'Mệnh':     'Văn Khúc tại Mệnh: Tài hoa đặc dị, khéo léo, nghệ thuật. Giỏi âm nhạc, nghệ thuật, viết lách.',
        'Quan Lộc': 'Văn Khúc tại Quan Lộc: Công việc học thuật, nghiên cứu. Dùng nghề bằng kiến thức đã học. Một số trường hợp đạt học vị cao.',
        '_': 'Văn Khúc tại đây: Nghệ thuật, tài hoa, văn chương. Cùng Văn Xương tạo bộ sao học vấn quý.',
    },

    // Tả Phù / Hữu Bật
    'Tả Phù': {
        'Mệnh':     'Tả Phù tại Mệnh: Được nhiều người hỗ trợ, có tướng lãnh đạo, dễ được cấp trên tin dùng.',
        'Nô Bộc':   'Tả Phù tại Nô Bộc: Quan hệ rộng, có nhiều cánh tay đắc lực. Luôn có người sẵn sàng giúp đỡ.',
        '_': 'Tả Phù tại đây: Quý nhân hỗ trợ, thêm lực mạnh cho cung này.',
    },
    'Hữu Bật': {
        'Mệnh':     'Hữu Bật tại Mệnh: Được nhiều người hỗ trợ, giỏi ngoại giao.',
        'Điền Trạch': 'Hữu Bật tại Điền Trạch: Có nhiều nhà, lúc ở nhà này lúc nhà kia. Nhà thường lệch một bên.',
        '_': 'Hữu Bật tại đây: Quý nhân trợ lực, tăng cường sức mạnh cung này.',
    },

    // Thiên Khôi / Thiên Việt
    'Thiên Khôi': {
        'Mệnh':     'Thiên Khôi tại Mệnh: Quý nhân bề trên giúp đỡ, thi cử đỗ đạt cao, IQ cao, học 1 biết 10. Người giản dị, cầu thị, thích đọc sách nghiên cứu. Cả nể, thiên về tình cảm.',
        '_': 'Thiên Khôi tại đây: Thiên Ất Quý Nhân — gặp quý nhân giúp đỡ, may mắn.',
    },
    'Thiên Việt': {
        'Phúc Đức': 'Thiên Việt tại Phúc Đức: Được hưởng phúc tổ tiên, công danh tài lộc được phù trì. Dòng họ nhiều người đỗ đạt, phát nam đinh.',
        '_': 'Thiên Việt tại đây: Quý nhân giúp đỡ, may mắn trong lĩnh vực cung này.',
    },

    // Lộc Tồn / Kình Dương / Đà La
    'Lộc Tồn': {
        'Mệnh':     'Lộc Tồn tại Mệnh: Tiền bạc dồi dào nhưng cô độc, ít bạn bè. Giữ của giỏi, chắt chiu.',
        'Tử Tức':   'Lộc Tồn tại Tử Tức: Ít con nhưng con cái giàu có, thành đạt. Đầu tư lớn cho con học hành.',
        '_': 'Lộc Tồn tại đây: Giữ tài lộc, ổn định nhưng cô lập. Tốt cho tích luỹ vật chất.',
    },
    'Kình Dương': {
        'Mệnh':     'Kình Dương tại Mệnh: Cứng rắn, có chí tiến thủ nhưng hay bị tổn thương. Cẩn thận tai nạn, mổ xẻ.',
        'Phu Thê':  'Kình Dương tại Phu Thê: Vợ chồng hay bất hoà, dễ xảy ra xung đột.',
        'Tài Bạch':  'Kình Dương tại Tài Bạch: Phải đấu tranh mạnh để kiếm tiền. Tiền đến từ mồ hôi nước mắt.',
        '_': 'Kình Dương tại đây: Hung sát tinh — hình thương, tai nạn, cứng đầu. Cần cẩn thận.',
    },
    'Đà La': {
        'Mệnh':     'Đà La tại Mệnh: Hay trì hoãn, lề mề nhưng bền bỉ. Cuộc đời nhiều trắc trở âm ỉ.',
        'Tài Bạch':  'Đà La tại Tài Bạch: Cần mưu mẹo để kiếm tiền. Tiền đến chậm nhưng bền.',
        '_': 'Đà La tại đây: Sát tinh âm ỉ, kéo chậm. Cần kiên nhẫn và cẩn thận.',
    },

    // Địa Không / Địa Kiếp
    'Địa Không': {
        'Mệnh':     'Địa Không tại Mệnh: Tư duy siêu thoát, dễ hướng đến tâm linh. Tiền bạc dễ mất.',
        'Nô Bộc':   'Địa Không tại Nô Bộc: Bạn bè tôi tớ xấu, tham lam, dễ lừa gạt.',
        '_': 'Địa Không tại đây: Hư không, mất mát, bất ngờ. Được mất đan xen.',
    },
    'Địa Kiếp': {
        'Mệnh':     'Địa Kiếp tại Mệnh: Cuộc đời hay gặp biến cố bất ngờ, vừa được vừa mất.',
        'Huynh Đệ': 'Địa Kiếp tại Huynh Đệ: Ít anh chị em, hay ly tán, xung đột, dễ liên quan mặt trái xã hội.',
        '_': 'Địa Kiếp tại đây: Bất ngờ, đột biến, hư hao. Cần đề phòng rủi ro.',
    },

    // Hỏa Tinh / Linh Tinh
    'Hỏa Tinh': {
        'Mệnh':     'Hỏa Tinh tại Mệnh: Tính nóng nảy, quyết đoán, nhanh nhẹn. Hay bị tai nạn liên quan đến lửa, điện.',
        'Phu Thê':  'Hỏa Tinh tại Phu Thê: Hòa khí gia đình chưa tốt, người hôn phối nóng tính.',
        'Tử Tức':   'Hỏa Tinh tại Tử Tức: Giảm số con, con cái ngang bướng, khó nuôi.',
        '_': 'Hỏa Tinh tại đây: Tính nóng, đột phát. Có thể gây tai nạn, xung đột nếu không kiểm soát.',
    },
    'Linh Tinh': {
        'Mệnh':     'Linh Tinh tại Mệnh: Thông minh đột xuất, nhanh trí nhưng cũng dễ bốc đồng, tai nạn.',
        'Phu Thê':  'Linh Tinh tại Phu Thê: Hòa khí gia đình chưa được tốt, dễ xảy ra xung đột.',
        '_': 'Linh Tinh tại đây: Đột phát, bất ngờ, hung hiểm. Cần đề phòng chấn thương.',
    },

    // Thiên Mã
    'Thiên Mã': {
        'Mệnh':     'Thiên Mã tại Mệnh: Người bận rộn, hay di chuyển, thích tự do. Phù hợp nghề đòi hỏi đi lại nhiều.',
        '_': 'Thiên Mã tại đây: Di chuyển, thay đổi, năng động. Tốt cho xuất ngoại và thay đổi tích cực.',
    },

    // Thiên Hình
    'Thiên Hình': {
        'Phu Thê':  'Thiên Hình tại Phu Thê: Áp đặt, gia trưởng. Vợ chồng hay xung đột, hòa khí chưa tốt.',
        '_': 'Thiên Hình tại đây: Hình phạt, nghiêm khắc, pháp luật. Cần chú ý tranh chấp và xung đột.',
    },

    // Thiên Diêu / Đào Hoa / Hồng Loan
    'Thiên Diêu': {
        'Phúc Đức': 'Thiên Diêu tại Phúc Đức: Dòng họ tín tâm thờ phụng tổ tiên. Mồ mả tổ tiên linh thiêng, xanh tốt. Dễ có năng lực tâm linh.',
        '_': 'Thiên Diêu tại đây: Đào hoa, lãng mạn, tình cảm. Cẩn thận chuyện thị phi tình ái.',
    },
    'Đào Hoa': {
        'Mệnh':     'Đào Hoa tại Mệnh: Người duyên dáng, hấp dẫn, nhiều duyên tình. Dễ gặp chuyện tình cảm phức tạp.',
        '_': 'Đào Hoa tại đây: Duyên lành, tình cảm, may mắn nhân duyên.',
    },
    'Hồng Loan': {
        'Mệnh':     'Hồng Loan tại Mệnh: Người duyên dáng, gặp nhiều cơ hội tình duyên. Đời sống tình cảm phong phú.',
        'Điền Trạch': 'Hồng Loan tại Điền Trạch: Nhà cửa nhiều cây xanh, được trang trí cẩn thận, thích thiên nhiên.',
        '_': 'Hồng Loan tại đây: May mắn tình duyên, gặp duyên lành, giải ách trừ tai.',
    },

    // Thiên Khốc / Thiên Hư
    'Thiên Khốc': {
        '_': 'Thiên Khốc tại đây: Tiếng khóc nhà trời — báo hiệu u uất, đau buồn, việc trái ý. Cần tâm lý vững trong giai đoạn này.',
    },
    'Thiên Hư': {
        '_': 'Thiên Hư tại đây: Hư không, ưu tư — báo hiệu lo lắng, trái ý, mất mát cảm xúc. Cần an tâm dưỡng tâm.',
    },

    // Tang Môn / Bạch Hổ / Điếu Khách / Phục Binh / Quan Phù
    'Tang Môn': {
        'Tài Bạch':  'Tang Môn tại Tài Bạch: Vất vả gánh nặng về tiền bạc cả đời. Phải đấu tranh kiên trì mới đảm bảo sinh nhai. Nên chọn ngành nghề bền vững.',
        'Phúc Đức': 'Tang Môn tại Phúc Đức: Hay phải lo chuyện mồ mả, thờ cúng. Cần quan tâm đến âm phần.',
        '_': 'Tang Môn tại đây: Mất mát, tang thương, gánh nặng. Cần cẩn thận trong giai đoạn này.',
    },
    'Bạch Hổ': {
        'Phúc Đức': 'Bạch Hổ tại Phúc Đức: Gánh vác để làm thịnh hưng dòng họ. Trong họ nhiều người thành đạt, có công danh.',
        '_': 'Bạch Hổ tại đây: Hung tinh — hình thương, tai nạn, bệnh tật. Rất tốt cho công việc nhưng bất lợi sức khoẻ.',
    },
    'Phục Binh': {
        'Huynh Đệ': 'Phục Binh tại Huynh Đệ: Anh em dễ lừa dối, không chân thành, hay khắc khẩu xung đột.',
        '_': 'Phục Binh tại đây: Ẩn họa, phục kích, bị lừa đảo. Cần đề phòng người xung quanh.',
    },
    'Quan Phù': {
        'Phu Thê':  'Quan Phù tại Phu Thê: Vợ chồng dễ bất hòa, nghi ngờ lẫn nhau. Dễ liên quan pháp luật, tranh chấp tài sản.',
        '_': 'Quan Phù tại đây: Kiện tụng, thị phi, pháp lý. Cẩn thận tranh chấp.',
    },

    // Ân Quang / Thiên Quý / Long Đức / Thiên Phúc
    'Ân Quang': {
        'Phúc Đức': 'Ân Quang tại Phúc Đức: Được thần linh che chở, sống thọ. Họ hàng đoàn kết, tổ tiên hiền lành. Biết làm từ thiện, được tổ tiên phù hộ.',
        '_': 'Ân Quang tại đây: Ân đức, phúc lành, được phù trì. Mang lại may mắn và sự bảo hộ.',
    },
    'Thiên Quý': {
        'Thiên Di':  'Thiên Quý tại Thiên Di: Ra ngoài hay gặp quý nhân, người hiền triết chỉ dạy. Được nhiều người kính trọng.',
        '_': 'Thiên Quý tại đây: Thanh cao, phước thiện, thủy chung. Được quý nhân giúp đỡ.',
    },
    'Long Đức': {
        'Phụ Mẫu':  'Long Đức tại Phụ Mẫu: Cha mẹ là người quân tử trượng nghĩa, nhân hậu, từ thiện, có nghề khéo.',
        '_': 'Long Đức tại đây: Đức hạnh cao quý, nhân phẩm tốt. Mang lại uy tín và sự kính trọng.',
    },
    'Thiên Phúc': {
        'Phúc Đức': 'Thiên Phúc tại Phúc Đức: Ấm phúc gia môn. Tổ tiên làm việc thiện, tiền kiếp đã từng tu hành. Cả đời đi đâu cũng gặp quý nhân.',
        '_': 'Thiên Phúc tại đây: Phúc lành, may mắn, được phù trì bởi tổ tiên.',
    },

    // Tấu Thư / Tam Thai / Bát Tọa
    'Tấu Thư': {
        'Quan Lộc': 'Tấu Thư tại Quan Lộc: Hành chính, viết lách, giảng dạy. Giỏi lý luận hùng biện, giảng dạy, thích nghiên cứu lịch sử văn hoá. Hướng nghề: giáo viên, luật sư, biên kịch.',
        '_': 'Tấu Thư tại đây: Sổ sách, giấy tờ, ấn tín. Liên quan đến hành chính và quản lý văn bản.',
    },
    'Tam Thai': {
        'Quan Lộc': 'Tam Thai tại Quan Lộc: May mắn về công danh, thi cử, chức vụ. Hay gặp may mắn trong nghề nghiệp.',
        '_': 'Tam Thai tại đây: May mắn, quý nhân, địa vị. Cát tinh tốt cho công danh.',
    },
    'Bát Tọa': {
        'Quan Lộc': 'Bát Tọa tại Quan Lộc: May mắn về công danh, thi cử, chức vụ. Hay gặp may mắn trong nghề nghiệp.',
        '_': 'Bát Tọa tại đây: Uy phong, địa vị, may mắn công danh.',
    },

    // Quả Tú / Cô Thần
    'Quả Tú': {
        'Quan Lộc': 'Quả Tú tại Quan Lộc: Độc lập trong công việc, không thích hùn vốn chung. Khó phát triển quan hệ xã hội, gặp khó phải tự mình giải quyết.',
        '_': 'Quả Tú tại đây: Cô đơn, độc lập. Làm một mình tốt hơn hợp tác.',
    },
    'Cô Thần': {
        'Tài Bạch':  'Cô Thần tại Tài Bạch: Giữ tiền tốt, của cải vững chắc. Chi tiêu hợp lý. Có nguồn thu nhập bí mật, một mình.',
        '_': 'Cô Thần tại đây: Cô đơn, bí mật, độc lập. Thích làm việc một mình.',
    },

    // Lực Sỹ / Địa Giải
    'Lực Sỹ': {
        'Tài Bạch':  'Lực Sỹ tại Tài Bạch: Vất vả tay chân lẫn đầu óc để kiếm tiền. Áp lực công việc nhiều nhưng dễ thay đổi. Làm thuần tuý chuyên môn.',
        '_': 'Lực Sỹ tại đây: Vất vả, cần cù, bền bỉ. Thành công nhờ nỗ lực thực sự.',
    },
    'Địa Giải': {
        'Tài Bạch':  'Địa Giải tại Tài Bạch: Hay bỏ tiền ra làm từ thiện, giúp đỡ cứu người. Tiền bị hao hụt đi một phần nhưng không đến mức nghèo khổ.',
        '_': 'Địa Giải tại đây: Giải ách, bố thí. Mất của để tránh tai.',
    },

    // Tuế Phá / Đại Hao / Tiểu Hao
    'Tuế Phá': {
        'Mệnh':     'Tuế Phá tại Mệnh: Tư duy ngược, bất nguyên tắc, thích phá bỏ cái cũ. Bé chống đối cha mẹ, lớn đi ngược tập thể. Hay lo âu suy nghĩ nhiều. Điểm mạnh: dám tư duy và đột phá.',
        '_': 'Tuế Phá tại đây: Phá vỡ, biến động, khó ổn định. Cần sắp xếp chỉn chu.',
    },
    'Đại Hao': {
        'Mệnh':     'Đại Hao tại Mệnh: Người nhanh nhẹn, lanh lợi, thích đấu tranh. Cả thèm chóng chán, dễ thay đổi. Tốt xấu cận kề, lúc phóng khoáng khi keo kiệt.',
        '_': 'Đại Hao tại đây: Hao tán, linh hoạt, thích phiêu lưu. Tiền vào nhiều cũng ra nhiều.',
    },
    'Tiểu Hao': {
        'Thiên Di':  'Tiểu Hao tại Thiên Di: Thích di chuyển, du lịch, khám phá. Dễ ăn chơi tiêu tiền khi ra ngoài.',
        '_': 'Tiểu Hao tại đây: Hao nhỏ, tiêu vặt. Cần kiểm soát chi tiêu.',
    },

    // Phong Cáo / Hoa Cái / Long Trì / Phượng Các
    'Phong Cáo': {
        'Phúc Đức': 'Phong Cáo tại Phúc Đức: Ông bà tổ tiên có danh chức địa vị. Dòng họ nhiều người thành đạt, có truyền thống học tốt.',
        '_': 'Phong Cáo tại đây: Danh tiếng, tước vị. Mang lại uy danh và sự công nhận.',
    },
    'Hoa Cái': {
        'Phu Thê':  'Hoa Cái tại Phu Thê: Vợ/chồng bảo thủ, điệu đà nhưng có kinh tế, kiến thức và dễ thành đạt.',
        '_': 'Hoa Cái tại đây: Nghệ thuật, tâm linh, trang nhã. Hướng đến sự tinh tế và độc đáo.',
    },
    'Long Trì': {
        'Phu Thê':  'Long Trì tại Phu Thê: Vợ chồng đẹp đôi, tương đắc. Người hôn phối quyền quý, thanh cao, có điều kiện kinh tế.',
        '_': 'Long Trì tại đây: Quyền quý, phú quý. Mang lại sự sang trọng và may mắn.',
    },
    'Phượng Các': {
        'Phu Thê':  'Phượng Các tại Phu Thê: Người hôn phối giỏi giang, xứng đôi. Gia đình nhà hôn phối có điều kiện và địa vị.',
        '_': 'Phượng Các tại đây: Thanh cao, xứng đôi. Tốt cho nhân duyên và hôn nhân.',
    },

    // Kiếp Sát / Phi Liêm / Thiên Quan
    'Kiếp Sát': {
        'Huynh Đệ': 'Kiếp Sát tại Huynh Đệ: Giảm số anh chị em. Anh chị em nóng tính, dễ bất hoà.',
        '_': 'Kiếp Sát tại đây: Kiếp nạn, mất mát đột ngột. Cần phòng rủi ro.',
    },
    'Phi Liêm': {
        'Điền Trạch': 'Phi Liêm tại Điền Trạch: Nhà ở nơi đất trũng thấp, hoặc vốn là ao hồ tôn lên. Hay chuyển nhà 2–3 lần mới yên gia đạo.',
        '_': 'Phi Liêm tại đây: Bất ổn, thay đổi chỗ ở. Mang tính lưu động cao.',
    },
    'Thiên Quan': {
        'Điền Trạch': 'Thiên Quan tại Điền Trạch: Được thừa hưởng đất đai tổ tiên, đất nhà thờ dòng họ. Tứ đại hoặc tam đại đồng đường.',
        '_': 'Thiên Quan tại đây: Quyền uy, nhà nước, chính quyền. Tốt cho công danh và pháp lý.',
    },

    // Thanh Long / Trực Phù / Đẩu Quân / Tướng Quân
    'Thanh Long': {
        'Tật Ách':  'Thanh Long tại Tật Ách: Giải trừ tai ách bệnh tật, họa đến có quý nhân giúp. Tang lễ sau này linh đình, mộ phần cát địa.',
        '_': 'Thanh Long tại đây: May mắn, giải ách. Tin vui, thành công trong giai đoạn này.',
    },
    'Trực Phù': {
        'Nô Bộc':   'Trực Phù tại Nô Bộc: Bạn bè, cấp dưới hiền lành, tốt tính, không ganh đua.',
        '_': 'Trực Phù tại đây: Thẳng thắn, trực tiếp. Mang lại sự chân thành và hỗ trợ.',
    },
    'Đẩu Quân': {
        'Nô Bộc':   'Đẩu Quân tại Nô Bộc: Khắt khe khó tính với bạn bè, ít bạn bè.',
        '_': 'Đẩu Quân tại đây: Khắt khe, tiêu chuẩn cao. Ít quan hệ nhưng chất lượng.',
    },
    'Tướng Quân': {
        'Nô Bộc':   'Tướng Quân tại Nô Bộc: Cần đề phòng bạn bè phản bội, môi trường làm việc tiềm ẩn rủi ro. Nếu đắc cách thì có bạn bè trong lực lượng vũ trang.',
        '_': 'Tướng Quân tại đây: Võ lực, uy quyền. Vừa mạnh mẽ vừa tiềm ẩn rủi ro xung đột.',
    },

    // Nguyệt Đức / Thiên Y / Thiên Hỷ / Giải Thần
    'Nguyệt Đức': {
        'Huynh Đệ': 'Nguyệt Đức tại Huynh Đệ: Anh chị em thuận hoà, hay giúp đỡ lẫn nhau.',
        '_': 'Nguyệt Đức tại đây: Âm đức, phúc lành. Giải trừ hung sát, mang lại bình an.',
    },
    'Thiên Y': {
        'Phúc Đức': 'Thiên Y tại Phúc Đức: Dòng họ nhiều người làm ngành y dược, cứu đời giúp người.',
        '_': 'Thiên Y tại đây: Chữa bệnh, y dược, phục hồi. Tốt cho sức khoẻ và chữa lành.',
    },
    'Thiên Hỷ': {
        'Tử Tức':   'Thiên Hỷ tại Tử Tức: May mắn bầu bí sinh con. Con cái vui vẻ, hoà thuận, khá giả.',
        '_': 'Thiên Hỷ tại đây: Hỷ sự, niềm vui, tin tốt. Mang lại may mắn và hạnh phúc.',
    },
    'Giải Thần': {
        'Phu Thê':  'Giải Thần tại Phu Thê: Vợ mặt mày thanh tú, nhà vợ khá giả, vợ giỏi kiếm tiền.',
        '_': 'Giải Thần tại đây: Giải ách, thoát nạn. Giảm thiểu tai họa.',
    },

    // Bệnh Phù / Thiên Không / Thiên Trù / Thiếu Âm
    'Bệnh Phù': {
        'Phụ Mẫu':  'Bệnh Phù tại Phụ Mẫu: Cha mẹ thường hay ốm đau bệnh tật, vất vả, không giàu có.',
        '_': 'Bệnh Phù tại đây: Ốm đau, suy yếu. Cần chú ý sức khoẻ bản thân và người thân.',
    },
    'Thiên Không': {
        'Tật Ách':  'Thiên Không tại Tật Ách: Tiêu trừ bệnh, có bệnh mau hết bệnh. Tốt cho sức khoẻ.',
        '_': 'Thiên Không tại đây: Hư không, thanh tịnh. Đôi khi mất mát nhưng cũng giải thoát.',
    },
    'Thiên Trù': {
        'Tật Ách':  'Thiên Trù tại Tật Ách: Dễ mắc bệnh từ ăn uống — tiêu hoá, bội thực, ngộ độc.',
        '_': 'Thiên Trù tại đây: Ăn uống, thực phẩm. Tốt cho việc hưởng thụ ẩm thực.',
    },
    'Thiếu Âm': {
        'Tử Tức':   'Thiếu Âm tại Tử Tức: Hưởng phúc từ con cái. Con cái hoà thuận, hiếu thảo. Dễ có một con gái.',
        '_': 'Thiếu Âm tại đây: Dịu dàng, âm nhu. Tốt cho tình cảm và gia đình.',
    },

    // Quốc Ấn / Đường Phủ / Hỷ Thần / Thiên Việt
    'Quốc Ấn': {
        'Nô Bộc':   'Quốc Ấn tại Nô Bộc: Bạn bè nhiều người giỏi giang, tài năng, có quyền có chức.',
        '_': 'Quốc Ấn tại đây: Ấn tín, quyền lực nhà nước. Tốt cho công danh và pháp lý.',
    },
    'Đường Phủ': {
        'Phúc Đức': 'Đường Phủ tại Phúc Đức: Được hưởng phúc tổ tiên, dòng họ có nhiều người giàu sang làm quan chức. Nhà thờ tổ lớn bề thế.',
        '_': 'Đường Phủ tại đây: Phúc lộc từ tổ tiên, sung túc. Mang lại sự thịnh vượng và ổn định.',
    },
    'Hỷ Thần': {
        'Phúc Đức': 'Hỷ Thần tại Phúc Đức: Yên ấm mồ mả, bình yên gia đạo họ tộc. Tổ tiên linh thiêng, con cháu giữ lễ hiếu.',
        '_': 'Hỷ Thần tại đây: Vui mừng, hỷ sự. Mang lại niềm vui và tin tốt lành.',
    },

    // Triệt Lộ / Tuần Không
    'Triệt Lộ': {
        'Phu Thê':  'Triệt Lộ tại Phu Thê: Vợ chồng khó đến với nhau, dễ đổ vỡ — khắc thân, khắc khẩu, khắc ý. Cần cùng chí hướng, cùng tích đức mới bền.',
        'Tử Tức':   'Triệt Lộ tại Tử Tức: Chậm muộn con, khó khăn đường con cái. Con cái sau này định cư ở xa.',
        '_': 'Triệt Lộ tại đây: Chặn đứng, cắt đứt. Lĩnh vực này bị trở ngại nặng nề.',
    },
    'Tuần Không': {
        '_': 'Tuần Không tại đây: Hư không, trống rỗng. Lĩnh vực này bị giảm sức mạnh hoặc khó thành hiện thực.',
    },

    // Lưu Sao
    'L. Thái Tuế':   { '_': 'Lưu Thái Tuế tại đây: Kiện tụng, thị phi, thay đổi bước ngoặt. Dễ trục trặc giấy tờ, mâu thuẫn, quyết định bất ngờ. Cần bình tĩnh khéo léo xử lý.' },
    'L. Tang Môn':   { '_': 'Lưu Tang Môn tại đây: Mất mát, buồn phiền, gánh nặng. Việc đại sự khó thành trong giai đoạn này.' },
    'L. Bạch Hổ':    { '_': 'Lưu Bạch Hổ tại đây: Rất tốt cho công việc nhưng bất lợi sức khoẻ. Cần lưu tâm ốm đau, hình thương, tai nạn bất ngờ.' },
    'L. Thiên Hư':   { '_': 'Lưu Thiên Hư tại đây: U uất, đau buồn, việc trái ý ngược lòng. Nhiều lo lắng tân toan.' },
    'L. Thiên Khốc': { '_': 'Lưu Thiên Khốc tại đây: Tiếng khóc, đau buồn, việc không mong muốn. Cần vững tâm.' },
    'L. Thiên Mã':   { '_': 'Lưu Thiên Mã tại đây: Bận rộn, di chuyển nhiều, thay đổi. Thuận xuất ngoại, công tác, du học.' },
    'L. Lộc Tồn':   { '_': 'Lưu Lộc Tồn tại đây: May mắn tiền bạc, tài chính dư giả, được chia lợi nhuận, cổ phần.' },
    'L. Kình Dương': { '_': 'Lưu Kình Dương tại đây: Sức khoẻ sa sút, tai nạn, ốm đau. Năm này cẩn thận ao hồ sông nước, tránh xa súc vật.' },
    'L. Đà La':      { '_': 'Lưu Đà La tại đây: Trì trệ, khó khăn âm ỉ, bệnh tật. Cẩn thận sức khoẻ và va chạm.' },
    'L. Hóa Lộc':   { '_': 'Phi Hóa Lộc tại đây: Nhiều hỷ tín, tin vui bất ngờ. Gia tăng tài lộc và may mắn cho cung này trong năm.' },
    'L. Hóa Quyền': { '_': 'Phi Hóa Quyền tại đây: Quyền lực, quyết đoán. Năm này tăng cường sức mạnh và ý chí cho lĩnh vực cung này.' },
    'L. Hóa Khoa':  { '_': 'Phi Hóa Khoa tại đây: Danh tiếng, học vấn. Cát lợi thi cử, công tác ở xa, giải ách trừ tai.' },
    'L. Hóa Kỵ':    { '_': 'Phi Hóa Kỵ tại đây: Kỵ thần — ách nạn, trở ngại. Cần đặc biệt cẩn thận với lĩnh vực cung này trong năm.' },
};

// =========================================
// DATABASE — Tràng Sinh theo cung
// =========================================
const LG_TRANG_SINH = {
    'Trường Sinh': 'Đất Trường Sinh: Sinh khí mạnh, khởi đầu tốt, phát triển bền lâu.',
    'Tràng Sinh':  'Đất Tràng Sinh: Sinh khí mạnh, khởi đầu tốt, phát triển bền lâu.',
    'Mộc Dục':    'Đất Mộc Dục: Còn non nớt, cần trau dồi học hỏi. Cung này liên quan y tế, chăm sóc, làm đẹp, sản phụ khoa.',
    'Quan Đới':   'Đất Quan Đới: Trưởng thành, bắt đầu lập nghiệp. Tích luỹ tài sản tốt.',
    'Lâm Quan':   'Đất Lâm Quan: Cường thịnh, đang ở đỉnh cao. Tích lũy được nhiều thành tựu.',
    'Đế Vượng':   'Đất Đế Vượng: Cực thịnh, vượng khí mạnh nhất. Sức khoẻ tốt, chịu khó, thọ trường.',
    'Suy':        'Đất Suy: Đang đi xuống. Thân hình nhỏ, lưng hơi gù, ôn hoà. Bé hay ốm.',
    'Bệnh':       'Đất Bệnh: Sức khỏe yếu, cần chú ý bệnh tật. Ít anh em (nếu ở Huynh Đệ).',
    'Tử':         'Đất Tử: Tĩnh lặng, dừng lại. Hay bất hoà ảnh hưởng thành tựu (nếu ở Phu Thê).',
    'Mộ':         'Đất Mộ: Tích trữ ẩn tàng. Chậm muộn nhưng bền. Giữ của tốt.',
    'Tuyệt':      'Đất Tuyệt: Tiêu tan, hư không. Tiền vào nhanh đi cũng nhanh.',
    'Thai':       'Đất Thai: Đang thai nghén, hình thành. Liên quan sinh sản, đường tiết niệu.',
    'Dưỡng':      'Đất Dưỡng: Nuôi dưỡng, hồi phục. Biết giúp người thì phúc báu đến.',
};

// =========================================
// THÂN CƯ — Ý nghĩa
// =========================================
const LG_THAN_CU = {
    'Mệnh':      'Thân cư Mệnh: Chú trọng bản thân, mạnh mẽ, tự lực, quyết đoán. Sức khoẻ ảnh hưởng nhiều đến cuộc đời.',
    'Phu Thê':   'Thân cư Phu Thê: Đặt nặng tình cảm, hôn nhân ảnh hưởng lớn đến cuộc đời. Cần có người bạn đời chia sẻ.',
    'Tài Bạch':  'Thân cư Tài Bạch: Ham kiếm tiền, giỏi tài chính. Vật chất là động lực chính trong cuộc sống.',
    'Thiên Di':  'Thân cư Thiên Di: Tự giác – Tự lập – Tự do. Sớm ly hương, thích đi xa, hướng ngoại, lạc quan phóng khoáng. Phù hợp: báo chí, du lịch, phân tích, điện ảnh, nghệ thuật, tổ chức sự kiện.',
    'Quan Lộc':  'Thân cư Quan Lộc: Coi trọng sự nghiệp, danh vọng là mục tiêu chính. Cần thành tựu công việc mới cảm thấy hạnh phúc.',
    'Phúc Đức': 'Thân cư Phúc Đức: Hưởng phúc tổ tiên, tâm linh, an nhàn. Nội tâm sâu sắc, hướng về tinh thần nhiều hơn vật chất.',
};

// =========================================
// ENGINE — Sinh văn luận giải
// =========================================

function _lookupStarText(db, starName, cungName) {
    const entry = db[starName];
    if (!entry) return null;
    return entry[cungName] || entry['_'] || null;
}

function _buildPalaceSection(palace, data) {
    const cungName = palace.cung_name || '';
    const diaChiLabel = palace.dia_chi ? ` (${palace.dia_chi})` : '';
    const stars = palace.stars || [];
    const adjStars = palace.adjective_stars || [];
    const luuStars = palace.luu_stars || [];

    const isMenh = palace.dia_chi === data.cung_menh;
    const isThan = palace.dia_chi === data.cung_than;

    let items = [];

    // Chính tinh
    const mainStarNames = new Set(['Tử Vi','Thiên Cơ','Thái Dương','Vũ Khúc','Thiên Đồng',
        'Liêm Trinh','Thiên Phủ','Thái Âm','Tham Lang','Cự Môn','Thiên Tướng','Thiên Lương','Thất Sát','Phá Quân']);

    stars.filter(s => mainStarNames.has(s.name)).forEach(s => {
        const txt = _lookupStarText(LG_CHINH_TINH, s.name, cungName);
        if (txt) items.push({ label: s.name, text: txt, cls: 'lg-item-main' });
    });

    // Nếu vô chính diệu — ghi chú
    const hasMain = stars.some(s => mainStarNames.has(s.name));
    if (!hasMain) {
        // Tìm cung xung chiếu
        const allPalaces = data.palaces || [];
        const diaChi12 = ['Tý','Sửu','Dần','Mão','Thìn','Tỵ','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi'];
        const myIdx = diaChi12.indexOf(palace.dia_chi);
        if (myIdx >= 0) {
            const xungIdx = (myIdx + 6) % 12;
            const xungChi = diaChi12[xungIdx];
            const xungPalace = allPalaces.find(p => p.dia_chi === xungChi);
            if (xungPalace) {
                const xungMain = (xungPalace.stars || []).filter(s => mainStarNames.has(s.name));
                if (xungMain.length > 0) {
                    items.push({
                        label: 'Vô Chính Diệu',
                        text: `Cung này không có chính tinh — dùng ${xungMain.map(s=>s.name).join(', ')} từ cung ${xungPalace.cung_name} xung chiếu để luận.`,
                        cls: 'lg-item-note'
                    });
                    xungMain.forEach(s => {
                        const txt = _lookupStarText(LG_CHINH_TINH, s.name, cungName);
                        if (txt) items.push({ label: s.name + ' (xung)', text: txt, cls: 'lg-item-main' });
                    });
                }
            }
        }
    }

    // Phụ tinh + tạp tinh + lưu sao
    const allAux = [
        ...stars.filter(s => !mainStarNames.has(s.name)),
        ...adjStars,
        ...luuStars.map(n => ({ name: n })),
    ];
    const seenAux = new Set();
    allAux.forEach(s => {
        if (seenAux.has(s.name)) return;
        seenAux.add(s.name);
        const txt = _lookupStarText(LG_PHU_TINH, s.name, cungName);
        if (txt) {
            const isLuu = s.name.startsWith('L.');
            items.push({ label: s.name, text: txt, cls: isLuu ? 'lg-item-luu' : 'lg-item-aux' });
        }
    });

    // Tràng sinh
    const ts = palace.trang_sinh;
    if (ts && LG_TRANG_SINH[ts]) {
        items.push({ label: ts, text: LG_TRANG_SINH[ts], cls: 'lg-item-ts' });
    }

    if (items.length === 0) return '';

    const badge = (isMenh && isThan) ? ' <span class="lg-badge menh">命</span><span class="lg-badge than">身</span>'
                : isMenh ? ' <span class="lg-badge menh">命</span>'
                : isThan ? ' <span class="lg-badge than">身</span>' : '';

    return `
    <details class="lg-palace-block" open>
        <summary class="lg-palace-header">
            <span class="lg-palace-name">${cungName}${diaChiLabel}${badge}</span>
            <span class="lg-palace-stars">${[...new Set([
                ...stars.filter(s=>mainStarNames.has(s.name)).map(s=>s.name),
                ...stars.filter(s=>!mainStarNames.has(s.name)).map(s=>s.name).slice(0,3)
            ])].join(' · ')}</span>
        </summary>
        <div class="lg-palace-body">
            ${items.map(it => `
            <div class="lg-item ${it.cls}">
                <span class="lg-item-label">${it.label}</span>
                <span class="lg-item-text">${it.text}</span>
            </div>`).join('')}
        </div>
    </details>`;
}

function _buildDaiVanSection(data) {
    const dv = data.dai_han;
    if (!dv) return '';
    const range = dv.range ? `${dv.range[0]}–${dv.range[1]} tuổi` : '';
    const diaChi = dv.dia_chi || dv.branch || '';
    return `
    <details class="lg-palace-block lg-daivan">
        <summary class="lg-palace-header">
            <span class="lg-palace-name">Đại Vận ${range}</span>
            <span class="lg-palace-stars">${diaChi}</span>
        </summary>
        <div class="lg-palace-body">
            <div class="lg-item lg-item-note">
                <span class="lg-item-label">Đại Vận</span>
                <span class="lg-item-text">Đại hạn ${range}${diaChi ? ` cung ${diaChi}` : ''}. Xem các sao chính tinh và phụ tinh tại cung đại vận để luận giải giai đoạn 10 năm này.</span>
            </div>
        </div>
    </details>`;
}

function _buildTieuHanSection(data) {
    const th = data.tieu_han;
    if (!th || !th.age) return '';
    const age = th.age;
    const diaChi = th.dia_chi || th.branch || '';
    const cungName = th.cung_name || '';
    const allPalaces = data.palaces || [];
    const thPalace = allPalaces.find(p => p.dia_chi === diaChi || p.cung_name === cungName);

    let items = [];
    if (thPalace) {
        const stars = [...(thPalace.stars||[]), ...(thPalace.adjective_stars||[]), ...(thPalace.luu_stars||[]).map(n=>({name:n}))];
        const seen = new Set();
        stars.forEach(s => {
            if (seen.has(s.name)) return;
            seen.add(s.name);
            const txt = _lookupStarText(LG_PHU_TINH, s.name, cungName || '') ||
                        _lookupStarText(LG_CHINH_TINH, s.name, cungName || '');
            if (txt) items.push(`<div class="lg-item lg-item-aux"><span class="lg-item-label">${s.name}</span><span class="lg-item-text">${txt}</span></div>`);
        });
    }

    return `
    <details class="lg-palace-block lg-tieuhan">
        <summary class="lg-palace-header">
            <span class="lg-palace-name">Tiểu Hạn ${age} tuổi</span>
            <span class="lg-palace-stars">${cungName} ${diaChi ? `(${diaChi})` : ''}</span>
        </summary>
        <div class="lg-palace-body">
            ${items.length ? items.join('') : '<div class="lg-item lg-item-note"><span class="lg-item-label">Ghi chú</span><span class="lg-item-text">Xem sao tại cung tiểu hạn để luận giải năm hiện tại.</span></div>'}
        </div>
    </details>`;
}

// =========================================
// MAIN — buildLuanGiaiHTML
// =========================================
function buildLuanGiaiHTML(data) {
    if (!data || !data.palaces) return '<p class="lg-empty">Chưa có dữ liệu lá số.</p>';

    const solar = data.birth?.solar || {};
    const lunar = data.birth?.lunar || {};
    const gender = data.gender || '';
    const isNam = gender.toLowerCase().includes('nam') || gender === 'male' || gender === 'm';

    // Xác định Thân cư
    const thanDiaChi = data.cung_than || '';
    const thanPalace = (data.palaces || []).find(p => p.dia_chi === thanDiaChi);
    const thanCung = thanPalace?.cung_name || '';
    const thanCuText = LG_THAN_CU[thanCung] || '';

    // Thứ tự cung hiển thị: Mệnh trước, sau đó 5 cung chính, rồi 6 cung còn lại
    const CUNG_ORDER = ['Mệnh','Quan Lộc','Tài Bạch','Phúc Đức','Thiên Di','Phụ Mẫu','Phu Thê','Tử Tức','Nô Bộc','Điền Trạch','Tật Ách','Huynh Đệ'];
    const palaceMap = {};
    (data.palaces || []).forEach(p => { palaceMap[p.cung_name] = p; });

    const palaceSections = CUNG_ORDER
        .map(cn => palaceMap[cn] ? _buildPalaceSection(palaceMap[cn], data) : '')
        .filter(Boolean)
        .join('');

    return `
    <div class="lg-root">
        <div class="lg-intro">
            <div class="lg-intro-title">Lá Số Tử Vi</div>
            <div class="lg-intro-info">
                Dương lịch: ${solar.day||'?'}/${solar.month||'?'}/${solar.year||'?'} &nbsp;·&nbsp;
                Âm lịch: ${lunar.day||'?'}/${lunar.month||'?'}/${lunar.year||'?'} &nbsp;·&nbsp;
                ${isNam ? 'Nam' : 'Nữ'}
            </div>
            ${thanCuText ? `<div class="lg-than-cu"><strong>Thân cư ${thanCung}:</strong> ${thanCuText}</div>` : ''}
        </div>

        <div class="lg-divider">── 12 Cung ──</div>
        ${palaceSections}

        <div class="lg-divider">── Vận Hạn ──</div>
        ${_buildDaiVanSection(data)}
        ${_buildTieuHanSection(data)}
    </div>`;
}

// Export cho tuvi-chart.js
window.buildLuanGiaiHTML = buildLuanGiaiHTML;
