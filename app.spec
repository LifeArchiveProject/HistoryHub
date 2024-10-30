# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('scripts', 'scripts'),
        ('routers', 'routers'),
        ('main.py', '.'),
        ('.venv/Lib/site-packages/pyecharts/datasets', 'pyecharts/datasets'),
        ('.venv/Lib/site-packages/pyecharts/render/templates', 'pyecharts/render/templates'),
    ],
    hiddenimports=[
        'fastapi',
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