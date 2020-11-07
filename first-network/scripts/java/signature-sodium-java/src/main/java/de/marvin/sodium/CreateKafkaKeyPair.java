package de.marvin.sodium;

import com.goterl.lazycode.lazysodium.LazySodiumJava;
import com.goterl.lazycode.lazysodium.SodiumJava;
import com.goterl.lazycode.lazysodium.exceptions.SodiumException;
import com.goterl.lazycode.lazysodium.interfaces.Sign;
import com.goterl.lazycode.lazysodium.utils.Key;
import com.goterl.lazycode.lazysodium.utils.KeyPair;

public class CreateKafkaKeyPair{
    public static void main(String[] args) {
        System.out.println(args[0]);
        try {
            SignatureUtil.generateSigningKeys(args[0]);
        } catch (Exception e) {
        }
    }
}