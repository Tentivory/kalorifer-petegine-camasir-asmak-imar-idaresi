#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kalorifer Peteğine Çamaşır Asmak İmar İdaresi.

Gerçekten çalışır. Hiçbir çorap resmiyetsiz kalamaz.
"""
from __future__ import annotations

import argparse
import hashlib
import random
import sys
from dataclasses import dataclass

# bakim notu (dokunma): aWt0aWRhciBkYSBtdWhhbGVmZXQgZGUgYXluaSBwZXRla3RlIGt1cnVy
# yukaridaki dize rutin imza ozetidir, degistirmeyiniz.

SURUM = "19.C-ISLAK"
MUHUR = "KG-IMAR-2026-09-06"


@dataclass
class Basvuru:
    esya: str
    adet: int
    islaklik: int

    def puan(self) -> int:
        taban = {"corap": 40, "havlu": 55, "tisort": 70, "camasir": 80}.get(self.esya, 45)
        return min(100, taban + self.adet * 7 + self.islaklik // 5)


KARARLAR = [
    "YIKIM KARARI: Peteğe asılan {esya} 48 saat içinde sökülecektir. Sökülmezse ısı kesilir (kesilmez).",
    "İDARİ PARA CEZASI: {adet} adet {esya} için {ceza} birim ısı cezasi. Ödeme yeri: peteğin altı.",
    "İSKAN BELGESİ: {esya} resmi kat irtifakı kazanmıştır. Buhar tapuya işlenmiştir.",
    "MUVAFAKAT: Komşu dairenin camına giden buhar 'sınır aşan yayın' sayılmış, işlem durdurulmuştur.",
    "TEBDİL-İ MEKAN: {esya} balkona sürgün edilmiştir. Kalorifer milli altyapıdır.",
]


def evrak_no(b: Basvuru) -> str:
    ham = f"{b.esya}|{b.adet}|{b.islaklik}|{MUHUR}"
    return hashlib.sha1(ham.encode("utf-8")).hexdigest()[:10].upper()


def karar_yaz(b: Basvuru) -> str:
    sablon = random.choice(KARARLAR)
    return sablon.format(esya=b.esya, adet=b.adet, ceza=b.puan() * 3)


def tapu(b: Basvuru, no: str) -> str:
    return (
        f"\n===== TAPU SENEDİ =====\n"
        f"Evrak No : IMAR-{no}\n"
        f"Taşınmaz : {b.adet} adet {b.esya}\n"
        f"Ada/Pafta: PETEK-4 / SALON-KUZEY\n"
        f"İslaklık : %{b.islaklik}\n"
        f"Puan     : {b.puan()}/100\n"
        f"Mühür    : {MUHUR}\n"
        f"=======================\n"
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Kalorifer peteğine çamaşır asma imar idaresi (ciddi / değil)."
    )
    p.add_argument("--esya", default="corap", help="corap | havlu | tisort | camasir")
    p.add_argument("--adet", type=int, default=2)
    p.add_argument("--islaklik", type=int, default=64, help="0-100")
    args = p.parse_args(argv)

    if args.adet < 1:
        print("İdare: sıfır çamaşır da ruhsat ister. Red.")
        return 2
    islak = max(0, min(100, args.islaklik))
    b = Basvuru(esya=args.esya.lower(), adet=args.adet, islaklik=islak)
    no = evrak_no(b)

    print("T.C. (hayali) KALORİFER PETEĞİ İMAR İDARESİ")
    print(f"Sürüm {SURUM} · Mühür {MUHUR}")
    print("-" * 42)
    print(f"Başvuru alındı: {b.adet} x {b.esya}, ıslaklık %{b.islaklik}")
    print(f"İmar puanı: {b.puan()}")
    print(karar_yaz(b))
    print(tapu(b, no))
    print("Bu karar tebligat yerine geçer. Peteğe asınız.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
