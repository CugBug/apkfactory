@echo off
if not %2 equ "f" (
apktool d %1
) else (
apktool d -f %1
)