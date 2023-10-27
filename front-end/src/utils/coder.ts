import JSEncrypt from 'jsencrypt'

const pubKey = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCTeeUgm3kuYTWbb3G25LnCTSuI\n4Kc6is+339ZoABc376sPWS5jr72yHs/tePxVCi4aKVmdRhBatXP5DoiZ9d4AETRE\nxAZWa5JMO9NxFE6Uu2Vtaj6xKyh1nMwEb+XgBI3d5f8MBSg//TrJYDwDa26G+P9g\neJzUCjr+h0ti6u83BQIDAQAB\n-----END PUBLIC KEY-----"

export function rsaEncrypt(text: string)
{
    const encryptor = new JSEncrypt()
    // const content = Base64.encode(text)
    encryptor.setPublicKey(pubKey)
    // console.log(encryptor.encrypt(text))
    return encryptor.encrypt(text)
}
