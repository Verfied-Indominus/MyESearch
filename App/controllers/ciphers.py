

def doubleCipher(plain_text,railkey,caesarkey):
    return caesarEncrypt(caesarkey,railFenceEncrypt(plain_text,railkey))

def doubleDeCipher(cipher_text,railkey,caesarkey):
    return caesarDecrypt(caesarkey,railFenceDecrypt(cipher_text,railkey))


def railFenceEncrypt(plainText, key):
    cipherText = ""
    array = [["" for x in range(len(plainText))] for y in range(len(key))]
    i = 1
    row = 0
    col = 0

    for char in plainText:
        if row + i < 0 or row + i >= len(array):
            i = i * -1

        array[row][col] = char
        row += i
        col += 1

    for list in array:
        cipherText += "".join(list)

    return cipherText

def railFenceDecrypt(cipherText, key):
    plainText = ""
    array = [["" for x in range(len(cipherText))] for y in range(len(key))]
    j = 0
    i = 1

    for current_row in range(0, len(array)):
        row = 0

        for col in range(0, len(array[row])):
            if row + i < 0 or row + i >= len(array):
                i = i * -1

            if row == current_row:
                array[row][col] += cipherText[j]
                j += 1

            row += i

    for index in range(0, len(cipherText)):
        for rows in array:
            if rows[index] != '':
                plainText += rows[index]

    return plainText


def caesarEncrypt(key,plaintext):
    cipherText = ""
    for char in plaintext:
        if ord(char) == 10:
            cipherText += chr(ord(char))
        else:
            cipherText += chr((ord(char) + key - 32) % 95 + 32)#chr((ord(char) + shift) % 127)
    return cipherText

def caesarDecrypt(key,cipherText):
    plainText = ""
    for char in cipherText:
        if ord(char) == 10:
            plainText += char
        else:
            plainText += chr((ord(char) - key - 32 + 95) % 95 + 32)#chr((ord(char) - shift) % 127)
    return plainText



