import CryptoJS from 'crypto-js';
import JSEncrypt from 'jsencrypt';

// 使用 AES 加密数据
// @param {string} data - 需要加密的数据
// @param {string} aesKey - 用于 AES 加密的密钥
// @return {string} - AES 加密后的数据
export function encryptData(data, aesKey) {
    // 生成一个随机的初始向量
    let iv = CryptoJS.lib.WordArray.random(128/8);
    let ivBase64 = CryptoJS.enc.Base64.stringify(iv);
    let encrypted = CryptoJS.AES.encrypt(data, CryptoJS.enc.Base64.parse(aesKey), { mode: CryptoJS.mode.CTR, padding: CryptoJS.pad.NoPadding, iv: iv });
    return { ciphertext: encrypted.toString(), iv: ivBase64 };
}

// 使用 RSA 公钥加密 AES 密钥
// @param {string} aesKey - 需要加密的 AES 密钥
// @param {string} rsaPublicKey - 用于 RSA 加密的公钥
// @return {string} - RSA 加密后的 AES 密钥
export function encryptAESKey(aesKey, rsaPublicKey) {
    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(rsaPublicKey);
    return encrypt.encrypt(aesKey);
}

// 导出一个函数，用于生成随机的 AES 密钥
// @return {string} - 生成的随机 AES 密钥
export function generateRandomAESKey() {
    // 初始化结果字符串
    let result = '';
    // 定义可能的字符集
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    // 获取字符集的长度
    const charactersLength = characters.length;
    // 循环生成 16 个随机字符
    for (let i = 0; i < 16; i++ ) {
        // 从字符集中随机选择一个字符，并添加到结果字符串中
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    // 对生成的随机 AES 密钥进行 Base64 编码
    let aesKey = CryptoJS.enc.Utf8.parse(result);
    // 返回 Base64 编码的 AES 密钥
    return CryptoJS.enc.Base64.stringify(aesKey);
}
