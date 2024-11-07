# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
yutto_exe = os.path.join(os.getcwd(), '.venv', 'Scripts', 'yutto.exe')
if not os.path.exists(yutto_exe):
    raise FileNotFoundError(f"找不到 yutto.exe: {yutto_exe}")

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[
        (yutto_exe, '.'),
    ],
    datas=[
        ('config/*', 'config'),
        ('scripts', 'scripts'),
        ('routers', 'routers'),
        ('main.py', '.'),
        ('.venv/Lib/site-packages/pyecharts/datasets', 'pyecharts/datasets'),
        ('.venv/Lib/site-packages/pyecharts/render/templates', 'pyecharts/render/templates'),
        ('.venv/Lib/site-packages/yutto', 'yutto'),
    ],
    hiddenimports=[
        'fastapi',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'uvicorn',
        'pydantic',
        'scripts',
        'routers',
        'yaml',
        'pymysql',
        'sqlite3',
        'jinja2',
        'pyecharts',
        'pandas',
        'openpyxl',
        'numpy',
        'pytz',
        'six',
        'python-dateutil',
        'requests',
        'email',
        'email.mime.text',
        'email.mime.multipart',
        'email.header',
        'pyecharts.render.templates',
        'yutto',
        'yutto.cli',
        'yutto.utils',
        'yutto.__main__',
        'aiofiles',
        'biliass',
        'dict2xml',
        'httpx',
        'h2',
        'hpack',
        'hyperframe',
        'socksio',
        'starlette',
        'starlette.middleware',
        'starlette.middleware.cors',
        'starlette.types',
        'fastapi.applications',
        'fastapi.routing',
        'fastapi.responses',
        'fastapi.params',
        'schedule',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BilibiliHistoryAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BilibiliHistoryAnalyzer'
)