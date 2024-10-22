const { app, BrowserWindow } = require('electron');
const path = require('path');
const log = require('electron-log');

const isDev = process.env.NODE_ENV === 'development';

const createWindow = () => {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.cjs'), // 确保路径正确
            nodeIntegration: false, // 禁用 Node.js 集成
            contextIsolation: true, // 启用上下文隔离
            enableRemoteModule: false, // 根据需要禁用远程模块
        },
    });

    if (isDev) {
        console.log('Loading development URL: http://localhost:5173');
        mainWindow.loadURL('http://localhost:5173');
        mainWindow.webContents.openDevTools(); // 可选：开发环境下打开开发者工具
    } else {
        const indexPath = path.join(app.getAppPath(), 'dist', 'index.html');
        console.log(`Loading file: ${indexPath}`);
        mainWindow.loadFile(indexPath);

    }
};

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

// 捕获未处理的异常并记录
process.on('uncaughtException', (error) => {
    log.error('Uncaught Exception:', error);
});
