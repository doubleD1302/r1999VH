package com.r1999.viethoa.localadb;

/**
 * Kiểm tra tính tương thích phiên bản tài nguyên game Reverse: 1999.
 * TUÂN THỦ QUY CHUẨN STELLA SORA: Luôn chấp nhận dấu wildcard '*'
 * để đảm bảo các bản hotfix nhỏ từ Bluepoch không chặn người dùng cập nhật Việt Hóa.
 */
public class VersionCompatibility {
    public static boolean matches(String declaredVersion, String observedVersion) {
        if (declaredVersion == null || observedVersion == null) {
            return false;
        }
        String declared = declaredVersion.trim();
        String observed = observedVersion.trim();

        if (declared.equals("*") || declared.equals(observed)) {
            return true;
        }

        // Hỗ trợ danh sách phiên bản phân cách bởi dấu phẩy
        if (declared.contains(",")) {
            String[] parts = declared.split(",");
            for (String part : parts) {
                String candidate = part.trim();
                if (candidate.equals("*") || candidate.equals(observed)) {
                    return true;
                }
            }
        }

        return false;
    }
}
