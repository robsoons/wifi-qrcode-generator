import argparse
from pathlib import Path

import qrcode
from PIL import Image


def escape_wifi_text(value: str) -> str:
    """Escape special characters according to Wi-Fi QR format."""
    escaped = value.replace("\\", "\\\\")
    for ch in [";", ",", ":", '"']:
        escaped = escaped.replace(ch, f"\\{ch}")
    return escaped


def build_wifi_payload(ssid: str, password: str, security: str, hidden: bool) -> str:
    ssid_safe = escape_wifi_text(ssid)
    hidden_flag = "true" if hidden else "false"

    if security == "nopass":
        return f"WIFI:T:nopass;S:{ssid_safe};H:{hidden_flag};;"

    pass_safe = escape_wifi_text(password)
    return f"WIFI:T:{security};S:{ssid_safe};P:{pass_safe};H:{hidden_flag};;"


def add_logo_center(qr_image: Image.Image, logo_path: Path, logo_scale: float) -> Image.Image:
    if not logo_path.exists():
        raise FileNotFoundError(f"Logo file not found: {logo_path}")

    base = qr_image.convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    max_logo_width = int(base.width * logo_scale)
    max_logo_height = int(base.height * logo_scale)
    logo.thumbnail((max_logo_width, max_logo_height), Image.LANCZOS)

    pos_x = (base.width - logo.width) // 2
    pos_y = (base.height - logo.height) // 2

    # White background behind the logo improves scanner reliability.
    padding = max(4, logo.width // 12)
    bg = Image.new("RGBA", (logo.width + 2 * padding, logo.height + 2 * padding), (255, 255, 255, 255))
    bg_x = pos_x - padding
    bg_y = pos_y - padding

    base.paste(bg, (bg_x, bg_y), bg)
    base.paste(logo, (pos_x, pos_y), logo)
    return base.convert("RGB")


def generate_wifi_qr(
    ssid: str,
    password: str,
    security: str,
    hidden: bool,
    output: Path,
    logo: Path | None,
    logo_scale: float,
    box_size: int,
    border: int,
    fill_color: str,
    back_color: str,
) -> Path:
    payload = build_wifi_payload(ssid=ssid, password=password, security=security, hidden=hidden)

    error_correction = qrcode.constants.ERROR_CORRECT_H if logo else qrcode.constants.ERROR_CORRECT_M

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    image = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    if logo:
        image = add_logo_center(image, logo, logo_scale)

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Wi-Fi QR code with optional company logo.")

    parser.add_argument("--ssid", required=True, help="Wi-Fi network name.")
    parser.add_argument("--password", default="", help="Wi-Fi password. Leave empty for open network.")
    parser.add_argument(
        "--security",
        default="WPA",
        choices=["WPA", "WEP", "nopass"],
        help="Wi-Fi security type.",
    )
    parser.add_argument("--hidden", action="store_true", help="Set if SSID is hidden.")
    parser.add_argument("--output", default="wifi_qr.png", help="Output image path.")
    parser.add_argument("--logo", default=None, help="Optional logo file path (PNG/JPG).")
    parser.add_argument(
        "--logo-scale",
        type=float,
        default=0.20,
        help="Logo size ratio relative to QR image (0.05 to 0.30 recommended).",
    )
    parser.add_argument("--box-size", type=int, default=10, help="QR pixel size for each module.")
    parser.add_argument("--border", type=int, default=4, help="QR border size in modules.")
    parser.add_argument("--fill-color", default="black", help="QR foreground color.")
    parser.add_argument("--back-color", default="white", help="QR background color.")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.security != "nopass" and not args.password:
        raise ValueError("Password is required when security is WPA or WEP.")

    if not 0.05 <= args.logo_scale <= 0.35:
        raise ValueError("--logo-scale must be between 0.05 and 0.35 for reliable scanning.")

    logo_path = Path(args.logo) if args.logo else None
    output_path = Path(args.output)

    result = generate_wifi_qr(
        ssid=args.ssid,
        password=args.password,
        security=args.security,
        hidden=args.hidden,
        output=output_path,
        logo=logo_path,
        logo_scale=args.logo_scale,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill_color,
        back_color=args.back_color,
    )

    print(f"QR code generated successfully: {result.resolve()}")


if __name__ == "__main__":
    main()
