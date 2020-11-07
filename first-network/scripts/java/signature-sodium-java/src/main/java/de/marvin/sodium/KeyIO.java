package de.marvin.sodium;

import com.goterl.lazycode.lazysodium.utils.Key;

import java.io.*;

public class KeyIO {
    public static void writeKeyToFile(Key key, String filePath) throws IOException {
        File file = new File(filePath);
        try (FileOutputStream fos = new FileOutputStream(file)) {
            fos.write(key.getAsBytes());
        } catch (FileNotFoundException e) {
            System.out.println("File not found" + e);
            throw e;
        } catch (IOException ioe) {
            System.out.println("Exception while writing file " + ioe);
            throw ioe;
        }
    }

    public static Key readKeyFromFile(String filePath) throws IOException {
        File file = new File(filePath);
        byte[] keyBytes;
        try (FileInputStream fis = new FileInputStream(file)) {
            keyBytes = new byte[(int) file.length()];
            if (fis.read(keyBytes) == -1) {
                throw new IOException("EOF reached while trying to read the whole file");
            }
        } catch (FileNotFoundException e) {
            System.out.println("File not found" + e);
            throw e;
        } catch (IOException ioe) {
            System.out.println("Exception while reading file " + ioe);
            throw ioe;
        }
        return Key.fromBytes(keyBytes);
    }
}
