import random
import os
import time


def crypting(text, cond):
    """
    Function to enable crypting or decrypting
    :param text : string
    :param cond : true = encrypt, false = decrypt
    :return crypted text : string
    """

    def text_to_ascii(text):
        """ Convert text into ascii codes """

        ascii_codes = []
        for char in text:
            ascii_code = str(ord(char))
            ascii_code = '0'*(3 - len(ascii_code)) + ascii_code
            ascii_codes.append(ascii_code)

        ascii_code = "".join(ascii_codes)
        return ascii_code

    def ascii_to_text(ascii_code):
        """ Convert ascii codes into text """

        split_ascii = [ascii_code[i:i+3] for i in range(0, len(ascii_code), 3)]
        text = []
        for ascii_code in split_ascii:
            char = chr(int(ascii_code))
            text.append(char)

        text = "".join(text)
        return text

    def increment_ascii(split_ascii, increment_code):
        """ Increment ascii code with constant number """

        shifted_ascii = []
        for ascii_code in split_ascii:
            ascii_code = str(int(ascii_code) + increment_code)
            ascii_code = '0' * (3 - len(ascii_code)) + ascii_code
            shifted_ascii.append(ascii_code)

        return shifted_ascii

    def increment_ascii_dynamic(split_ascii):
        """ increment ascii with number depend on the next element """

        for i in range(0, len(split_ascii)-1):
            split_ascii[i] = str(int(int(split_ascii[i]) + int(split_ascii[i+1]) // 5))
            split_ascii[i] = '0' * (3 - len(split_ascii[i])) + split_ascii[i]

        return split_ascii

    def decrement_ascii_dynamic(split_ascii):
        """ decrement ascii number depend on the next element """

        i = len(split_ascii) - 2
        while i >= 0:
            split_ascii[i] = str(int(int(split_ascii[i]) - int(split_ascii[i + 1]) // 5))
            split_ascii[i] = '0' * (3 - len(split_ascii[i])) + split_ascii[i]

            i -= 1

        return split_ascii

    def add_random_number(split_ascii, start_index):
        """ add random ascii at specified index """

        random_text = str(os.urandom(2))[:5]  # len is 5 char, 15 ascii symbols
        random_ascii = text_to_ascii(random_text)
        split_random = [random_ascii[i:i + 3] for i in range(0, len(random_ascii), 3)]
        split_ascii = split_ascii[:start_index] + split_random + split_ascii[start_index:]

        return split_ascii

    def remove_random_number(split_ascii, start_index):
        """ Remove random ascii from specified index """

        split_ascii[start_index: (start_index+5)] = []

        return split_ascii

    def shifting_ascii(split_ascii, shift_code):
        """ shift ascii code according to code """

        split_shift_code = [shift_code[i:i + 2] for i in range(0, len(shift_code), 2)]
        split_shift_code.insert(0, 0)

        for j in range(1, len(split_shift_code)):

            shift_code = int(split_shift_code[j])
            padding = int(split_shift_code[j-1])

            if (shift_code + padding) < len(split_ascii):

                temp = split_ascii[padding]
                for i in range(0, shift_code):
                    split_ascii[padding + i] = split_ascii[padding + i + 1]

                split_ascii[padding + shift_code] = temp

        return split_ascii

    def de_shifting_ascii(split_ascii, shift_code):
        """ de-shift ascii code according to code """

        split_shift_code = [shift_code[i:i + 2] for i in range(0, len(shift_code), 2)]
        split_shift_code.insert(0, 0)
        split_shift_code = list(reversed(split_shift_code))

        for j in range(0, len(split_shift_code)-1):

            shift_code = int(split_shift_code[j])
            padding = int(split_shift_code[j+1])

            if (shift_code + padding) < len(split_ascii):

                temp = split_ascii[padding + shift_code]

                i = shift_code-1
                while i >= 0:
                    split_ascii[padding + i + 1] = split_ascii[padding + i]
                    i -= 1

                split_ascii[padding] = temp

        return split_ascii

    def masking(split_ascii):
        """ Mask ascii code with the next element """

        for i in range(0, len(split_ascii)-1):
            split_ascii[i] = str(int(split_ascii[i]) ^ int(split_ascii[i+1]))
            split_ascii[i] = '0' * (3 - len(split_ascii[i])) + split_ascii[i]

        return split_ascii

    def de_masking(split_ascii):
        """ de-mask ascii code with the next element """

        i = len(split_ascii)-2
        while i >= 0:
            split_ascii[i] = str(int(split_ascii[i]) ^ int(split_ascii[i + 1]))
            split_ascii[i] = '0' * (3 - len(split_ascii[i])) + split_ascii[i]
            i -= 1

        return split_ascii

    def encrypt_setting(passcode):
        """ Create encryption settings """

        def create_shift_code(passcode, cond):

            if cond:
                shift_code = str(random.randrange(0, (len(passcode) // 2)))
            else:
                shift_code = str(random.randrange((len(passcode) // 2 + 1), (len(passcode) + 1)))

            shift_code = '0' * (2 - len(shift_code)) + shift_code
            return shift_code

        increment_code = str(random.randrange(5, len(passcode)+1))[:2]
        increment_code = '0' * (2 - len(increment_code)) + increment_code

        # Set up adding index
        random_number_added = 3
        start_index_1 = str(int(len(passcode) / random_number_added))
        start_index_1 = '0' * (2 - len(start_index_1)) + start_index_1
        start_index_2 = str(int(len(passcode) / random_number_added) * 2)
        start_index_2 = '0' * (2 - len(start_index_2)) + start_index_2
        start_index_3 = str(int(len(passcode) / random_number_added) * 3)
        start_index_3 = '0' * (2 - len(start_index_3)) + start_index_3

        # Set up shifting code
        shift_codes = []
        for i in range(0, random.randrange(1, 5)):
            shift_code = create_shift_code(passcode, True)
            shift_codes.append(shift_code)
            shift_code = create_shift_code(passcode, False)
            shift_codes.append(shift_code)

        shift_codes = "".join(shift_codes)

        setting = increment_code + start_index_1 + start_index_2 + start_index_3 + shift_codes
        setting = setting + str(len(setting))

        return setting

    def decrypt_setting(encrypted_passcode):
        """ decrypt the encryption settings """

        setting_length = encrypted_passcode[-2:]
        setting = encrypted_passcode[-int(setting_length)-2:-2]

        increment_code = setting[:2]
        start_index_1 = setting[2:4]
        start_index_2 = setting[4:6]
        start_index_3 = setting[6:8]
        shift_codes = setting[8:]

        return int(increment_code), int(start_index_1), int(start_index_2), int(start_index_3), str(shift_codes)

    def validity_code(encrypted_passcode):

        temp = 0
        for x in encrypted_passcode:
            temp += int(x)

        validity_code = str(temp % int(encrypted_passcode[-2:]))
        validity_code = '0' * (2 - len(validity_code)) + validity_code

        return validity_code

    def validity_check(encrypted_passcode):

        validity_code = encrypted_passcode[:2]
        encrypted_passcode = encrypted_passcode[2:]

        temp = 0
        for x in encrypted_passcode:
            temp += int(x)

        return int(validity_code) == (temp % int(encrypted_passcode[-2:]))

    def encrypt(passcode):
        """ Encrypt passcode """

        # Generate the settings
        encrypted_setting = encrypt_setting(passcode)
        increment_code, start_index_1, start_index_2, start_index_3, shift_code = decrypt_setting(encrypted_setting)

        ascii_code = text_to_ascii(passcode)
        split_ascii = [ascii_code[i:i + 3] for i in range(0, len(ascii_code), 3)]

        # Step - 1 attempt increment
        split_ascii = increment_ascii(split_ascii, increment_code=increment_code)

        # Step - 2 attempt adding random ascii in several places
        split_ascii = add_random_number(split_ascii, start_index_1)
        split_ascii = add_random_number(split_ascii, start_index_2)
        split_ascii = add_random_number(split_ascii, start_index_3)

        # Step - 3 attempt shifting
        split_ascii = shifting_ascii(split_ascii, shift_code)

        # Step - 4 attempt dynamic increment
        split_ascii = increment_ascii_dynamic(split_ascii)

        # Step - 5 attempt masking
        split_ascii = masking(split_ascii)

        ascii_code = "".join(split_ascii)

        ascii_code = ascii_code + encrypted_setting
        ascii_code = validity_code(ascii_code) + ascii_code

        return ascii_code

    def decrypt(encrypted_passcode):
        """ decrypt encrypted passcode """

        if not validity_check(encrypted_passcode):
            return "decrypting failed, invalid code"

        else:
            encrypted_passcode = encrypted_passcode[2:]

        # Get the settings
        increment_code, start_index_1, start_index_2, start_index_3, shift_code = decrypt_setting(encrypted_passcode)
        setting_length = int(encrypted_passcode[-2:])

        ascii_code = encrypted_passcode[:-setting_length-2]
        split_ascii = [ascii_code[i:i + 3] for i in range(0, len(ascii_code), 3)]

        # Step - 1 attempt de masking
        split_ascii = de_masking(split_ascii)

        # Step - 2 attempt dynamic decrement
        split_ascii = decrement_ascii_dynamic(split_ascii)

        # Step - 3 attempt shifting
        de_shifting_ascii(split_ascii, shift_code)

        # Step - 4 attempt remove random ascii
        split_ascii = remove_random_number(split_ascii, start_index_3)
        split_ascii = remove_random_number(split_ascii, start_index_2)
        split_ascii = remove_random_number(split_ascii, start_index_1)

        # Step - 5 attempt decrement
        split_ascii = increment_ascii(split_ascii, increment_code=-increment_code)

        ascii_code = "".join(split_ascii)
        text = ascii_to_text(ascii_code)
        return text

    if cond:
        crypted_text = encrypt(text)
    else:
        crypted_text = decrypt(text)

    return crypted_text


def statistic_test():
    plain = "Pada tugas kali ini, mahasiswa diminta membuat program yang mensimulasikan transformasi linier untuk melakukan operasi translasi, refleksi, dilatasi, rotasi, dan sebagainya pada sebuah bidang 2D.Bidang dibuat dengan mendefinisikan sekumpulan titik sudut lalu membuat bidang dari titik-titik tersebut.Program akan memiliki dua buah window, window pertama (command prompt) berfungsi untukmenerima input dari user, sedangkan window kedua (GUI) berfungsi untuk menampilkan outputberdasarkan input dari user. Kedua window ini muncul ketika user membuka file executable.Saat program baru mulai dijalankan, program akan menerima input N, yaitu jumlah titik yang akanditerima. Berikutnya, program akan menerima input N buah titik tersebut (pasangan nilai x dan y). Setelahitu program akan menampilkan output sebuah bidang yang dibangkitkan dari titik-titik tersebut. Selain itujuga ditampilkan dua buah garis, yaitu sumbu x dan sumbu y. Nilai x dan y memiliki rentang minimal -500 pixel dan maksikum 500 pixel. Pastikan window GUI yang Anda buat memiliki ukuran yang cukupuntuk menampilkan kedua sumbu dari ujung ke ujung.Berikutnya, program dapat menerima input yang didefinisikan pada tabel dibawah.Input Keterangan"

    constant = 100
    tic = time.clock()
    for _ in range(0, constant):
        crypted = crypting(plain, True)
    toc = time.clock()
    print("Time elapsed:", (toc - tic), "second(s)")
    print("letter processed : ", constant*len(plain))
    print("speed : ", constant*len(plain)/(toc-tic)/1024,"(kb / sec)")
    print()

    tic = time.clock()
    for _ in range(0, constant):
        decrypted = crypting(crypted, False)
    toc = time.clock()
    print("Time elapsed:", (toc - tic), "second(s)")
    print("letter processed : ", constant*len(crypted))
    print("speed : ", constant*len(crypted)/(toc-tic)/1024,"(kb / sec)")



    print()
    print()
    print("ratio plain : encrypted", len(crypted)/len(plain))
    if plain == decrypted:
        print("encrypt decrypt success")


"""
Time elapsed: 0.88025390522035 second(s)
letter processed :  120900
speed :  134.12767106150466 (kb / sec)

Time elapsed: 0.7277666147105847 second(s)
letter processed :  369300
speed :  495.5497050292966 (kb / sec)

ratio plain : encrypted 3.054590570719603
"""

def __main__():
    cont = True
    while cont:
        choice = input("input 'encrypt' or 'decrypt' : ")
        if 'encrypt' in choice:
            plain = input("input your text : \n")
            print()
            print("heres the encrypted:")
            print(crypting(plain, True))

        elif 'decrypt' in choice:
            encrypted = input("input encrypted text : \n")
            print()
            print("heres the decrypted:")
            print(crypting(encrypted, False))

        else:
            print("no such feature...")

        again = input("\nwanna try again ? <yes / no> : ")
        cont = "yes" in again

    print("\n(press any key to exit")
    os.system("pause")


__main__()