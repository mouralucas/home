// PEM encoded X.509 key
const publicKey =
    `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAunF5aDa6HCfLMMI/MZLT
5hDk304CU+ypFMFiBjowQdUMQKYHZ+fklB7GpLxCatxYJ/hZ7rjfHH3Klq20/Y1E
bYDRopyTSfkrTzPzwsX4Ur/l25CtdQldhHCTMgwf/Ev/buBNobfzdZE+Dhdv5lQw
KtjI43lDKvAi5kEet2TFwfJcJrBiRJeEcLfVgWTXGRQn7gngWKykUu5rS83eAU1x
H9FLojQfyia89/EykiOO7/3UWwd+MATZ9HLjSx2/Lf3g2jr81eifEmYDlri/OZp4
OhZu+0Bo1LXloCTe+vmIQ2YCX7EatUOuyQMt2Vwx4uV+d/A3DP6PtMGBKpF8St4i
GwIDAQAB
-----END PUBLIC KEY-----`;

async function importPublicKeyAndEncrypt(plaintext, encode) {

    try {
        const pub = await importPublicKey(publicKey);
        const encrypted = await encryptRSA(pub, new TextEncoder().encode(encode));
        const encryptedBase64 = window.btoa(ab2str(encrypted));
        const encrypted_return = await encryptedBase64.replace(/(.{64})/g, "$1\n");
        $('#'+plaintext).attr('value', encrypted_return);
        return encrypted_return;
    } catch(error) {
        console.log(error);
    }
}

async function importPublicKey(spkiPem) {
    return await window.crypto.subtle.importKey(
        "spki",
        getSpkiDer(spkiPem),
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["encrypt"]
    );
}

async function encryptRSA(key, plaintext) {
    let encrypted = await window.crypto.subtle.encrypt(
        {
            name: "RSA-OAEP"
        },
        key,
        plaintext
    );
    return encrypted;
}

function getSpkiDer(spkiPem){
    const pemHeader = "-----BEGIN PUBLIC KEY-----";
    const pemFooter = "-----END PUBLIC KEY-----";
    var pemContents = spkiPem.substring(pemHeader.length, spkiPem.length - pemFooter.length);
    var binaryDerString = window.atob(pemContents);
    return str2ab(binaryDerString);
}

//
// Helper
//

// https://stackoverflow.com/a/11058858
function str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}

function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
}




// PEM encoded PKCS#8 key
const privateKey =
    `-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC6cXloNrocJ8sw
wj8xktPmEOTfTgJT7KkUwWIGOjBB1QxApgdn5+SUHsakvEJq3Fgn+FnuuN8cfcqW
rbT9jURtgNGinJNJ+StPM/PCxfhSv+XbkK11CV2EcJMyDB/8S/9u4E2ht/N1kT4O
F2/mVDAq2MjjeUMq8CLmQR63ZMXB8lwmsGJEl4Rwt9WBZNcZFCfuCeBYrKRS7mtL
zd4BTXEf0UuiNB/KJrz38TKSI47v/dRbB34wBNn0cuNLHb8t/eDaOvzV6J8SZgOW
uL85mng6Fm77QGjUteWgJN76+YhDZgJfsRq1Q67JAy3ZXDHi5X538DcM/o+0wYEq
kXxK3iIbAgMBAAECggEASlJj0ExIomKmmBhG8q8SM1s2sWG6gdQMjs6MEeluRT/1
c2v79cq2Dum5y/+UBl8x8TUKPKSLpCLs+GXkiVKgHXrFlqoN+OYQArG2EUWzuODw
czdYPhhupBXwR3oX4g41k/BsYfQfZBVzBFEJdWrIDLyAUFWNlfdGIj2BTiAoySfy
qmamvmW8bsvc8coiGlZ28UC85/Xqx9wOzjeGoRkCH7PcTMlc9F7SxSthwX/k1VBX
mNOHa+HzGOgO/W3k1LDqJbq2wKjZTW3iVEg2VodjxgBLMm0MueSGoI6IuaZSPMyF
EM3gGvC2+cDBI2SL/amhiTUa/VDlTVw/IKbSuar9uQKBgQDd76M0Po5Lqh8ZhQ3o
bhFqkfO5EBXy7HUL15cw51kVtwF6Gf/J2HNHjwsg9Nb0eJETTS6bbuVd9bn884Jo
RS986nVTFNZ4dnjEgKjjQ8GjfzdkpbUxsRLWiIxuOQSpIUZGdMi2ctTTtspvMsDs
jRRYdYIQCe/SDsdHGT3vcUCybwKBgQDXDz6iVnY84Fh5iDDVrQOR4lYoxCL/ikCD
JjC6y1mjR0eVFdBPQ4j1dDSPU9lahBLby0VyagQCDp/kxQOl0z2zBLRI4I8jUtz9
/9KW6ze7U7dQJ7OTfumd5I97OyQOG9XZwKUkRgfyb/PAMBSUSLgosi38f+OC3IN3
qlvHFzvxFQKBgQCITpUDEmSczih5qQGIvolN1cRF5j5Ey7t7gXbnXz+Umah7kJpM
IvdyfMVOAXJABgi8PQwiBLM0ySXo2LpARjXLV8ilNUggBktYDNktc8DrJMgltaya
j3HNd2IglD5rjfc2cKWRgOd7/GlKcHaTEnbreYhfR2sWrWLxJOyoMfuVWwKBgFal
CbMV6qU0LfEo8aPlBN8ttVDPVNpntP4h0NgxPXgPK8Pg+gA1UWSy4MouGg/hzkdH
aj9ifyLlCX598a5JoT4S0x/ZeVHd/LNI8mtjcRzD6cMde7gdFbpLb5NSjIAyrsIA
X4hxvpnqiOYRePkVIz0iLGziiaMbfMwlkrxvm/LRAoGBALPRbtSbE2pPgvOHKHTG
Pr7gKbmsWVbOcQA8rG801T38W/UPe1XtynMEjzzQ29OaVeQwvUN9+DxFXJ6Yvwj6
ih4Wdq109i7Oo1fDnMczOQN9DKch2eNAHrNSOMyLDCBm++wbyHAsS2T0VO8+gzLA
BviZm5AFCQWfke4LZo5mOS10
-----END PRIVATE KEY-----`;


async function importPrivateKeyAndDecrypt(value) {
    // A ciphertext produced with the first code
    const ciphertextB64 = value;

    try {
        const priv = await importPrivateKey(privateKey);
        return await decryptRSA(priv, str2ab(window.atob(ciphertextB64)));
    } catch(error) {
        console.log(error);
    }
}

async function importPrivateKey(pkcs8Pem) {
    return await window.crypto.subtle.importKey(
        "pkcs8",
        getPkcs8Der(pkcs8Pem),
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["decrypt"]
    );
}

async function decryptRSA(key, ciphertext) {
    let decrypted = await window.crypto.subtle.decrypt(
        {
            name: "RSA-OAEP"
        },
        key,
        ciphertext
    );
    return new TextDecoder().decode(decrypted);
}

function getPkcs8Der(pkcs8Pem){
    const pemHeader = "-----BEGIN PRIVATE KEY-----";
    const pemFooter = "-----END PRIVATE KEY-----";
    var pemContents = pkcs8Pem.substring(pemHeader.length, pkcs8Pem.length - pemFooter.length);
    var binaryDerString = window.atob(pemContents);
    return str2ab(binaryDerString);
}