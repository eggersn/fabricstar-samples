package de.marvin.sodium;

import com.goterl.lazycode.lazysodium.LazySodiumJava;
import com.goterl.lazycode.lazysodium.SodiumJava;
import com.goterl.lazycode.lazysodium.exceptions.SodiumException;
import com.goterl.lazycode.lazysodium.interfaces.Sign;
import com.goterl.lazycode.lazysodium.utils.Key;
import com.goterl.lazycode.lazysodium.utils.KeyPair;

import java.io.*;

import static de.marvin.sodium.KeyIO.readKeyFromFile;
import static de.marvin.sodium.KeyIO.writeKeyToFile;

public class SignatureUtil {

    private static LazySodiumJava lazySodium = new LazySodiumJava(new SodiumJava());

    public static KeyPair getOrGenerateSigningKeys() throws IOException, SodiumException {
        return getOrGenerateSigningKeys("");
    }

    public static KeyPair generateSigningKeys() throws SodiumException, IOException {
        return generateSigningKeys("");
    }

    public static KeyPair getOrGenerateSigningKeys(String pathToKeys) throws IOException, SodiumException {
        try {
            Key publicKey = readKeyFromFile(pathToKeys + "public.key");
            Key secretKey = readKeyFromFile(pathToKeys + "secret.key");
            return new KeyPair(publicKey, secretKey);
        } catch (IOException e) {
            System.out.println("Generate new key pair.");
        }
        return generateSigningKeys(pathToKeys);
    }

    public static KeyPair generateSigningKeys(String pathToKeys) throws SodiumException, IOException {
        KeyPair kp = lazySodium.cryptoSignKeypair();
        Key publicKey = kp.getPublicKey();
        Key secretKey = kp.getSecretKey();
        if (!lazySodium.cryptoSignKeypair(publicKey.getAsBytes(), secretKey.getAsBytes())) {
            throw new SodiumException("Could not generate a signing keypair.");
        }
        writeKeyToFile(publicKey, pathToKeys + "public.key");
        writeKeyToFile(secretKey, pathToKeys + "secret.key");
        return kp;
    }

    public static byte[] sign(byte[] messageBytes, Key secretKey){
        return sign(messageBytes, secretKey.getAsBytes());
    }

    public static boolean verifySign(byte[] messageBytes, byte[] signature, Key publicKey){
        return verifySign(messageBytes, signature, publicKey.getAsBytes());
    }

    public static byte[] sign(byte[] messageBytes, byte[] secretKey){
        byte[] signatureBytes = new byte[Sign.BYTES];
        lazySodium.cryptoSignDetached(signatureBytes, messageBytes, messageBytes.length,  secretKey);
        return signatureBytes;
    }

    public static boolean verifySign(byte[] messageBytes, byte[] signature, byte[] publicKey){
        return lazySodium.cryptoSignVerifyDetached(signature, messageBytes, messageBytes.length, publicKey);
    }
}
