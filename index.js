const ENCRYPTION_KEY = "QWERTY";
const match_brackets = /([^\[]*)]/;
const match_inner_quote = /"(.*)"/;

function encryption(input_text, encrypt) {
    let output = [];
    const KEY_MAX_INDEX = ENCRYPTION_KEY.length;

    for (const [index, c] of Array.from(input_text).entries()) {
        CodePointInput = c.charCodeAt(0);
        codePointKey = ENCRYPTION_KEY[index % KEY_MAX_INDEX].codePointAt(0);

        let output_char = '';
        if (encrypt) {
            output_char = String.fromCodePoint(CodePointInput + codePointKey);
        }
        else {
            output_char = String.fromCodePoint(CodePointInput - codePointKey);
        }
        output.push(output_char)
    }

    return output.join('');
}

function downloadFile(text, filename) {
    const bb = new Blob([text]);
    let a = document.createElement('a');
    a.download = filename;
    a.href = window.URL.createObjectURL(bb);
    a.click();
}

function convertLine(line, encrypt) {
    if (line[0] == "\0") {
        console.log("null line found");
        return null;
    }

    if (line[0] === " ") {
        return null;
    }

    let match;
    if ((match = match_brackets.exec(line)) !== null) {
        const changed_text = encryption(match[1], encrypt);
        return `[${changed_text}]\n`
    }
    else {
        const [key, value] = line.split("=");
        const changed_key = encryption(key, encrypt);
        if (!changed_key) {
            return null;
        }
        let changed_val;
        if ((match = match_inner_quote.exec(value)) !== null) {
            changed_val = encryption(match[1], encrypt);
        }
        else {
            changed_val = "";
        }

        return `${changed_key}="${changed_val}"\n`;
    }
}

//#Source https://bit.ly/2neWfJ2 
const splitLines = str => str.split(/\r?\n/);

function readSave(text, encrypt) {
    let output = []
    for (line of splitLines(text)) {
        let converted = convertLine(line, encrypt);
        if (converted === null) {
            continue
        }

        output.push(converted);
    }
    return output.join('');
}

function handleDecryptionOfFile(e) {
    const is_encrypt = e.currentTarget.id == "encrypt";
    const fileList = this.files;
    if (fileList.length === 0) {
        console.log("No files selected");
        return;
    }
    const file = fileList[0];
    const reader = new FileReader();
    reader.onload = function() {
        const changedText = readSave(reader.result, is_encrypt);
        let filename = file.name;
        if (is_encrypt) {
            filename = `${file.name}.sav`;
        }
        else {
            filename = `${file.name}.decoded.txt`;
        }
        downloadFile(changedText, filename);
    };
    reader.readAsText(file);
    this.value = "";
}

const decryptInput = document.getElementById('decrypt');
const encryptInput = document.getElementById('encrypt');
const encryptedArea = document.getElementById('encrypted');
const decryptedArea = document.getElementById('decrypted');

decryptInput.addEventListener("change", handleDecryptionOfFile, false);

encryptInput.addEventListener("change", handleDecryptionOfFile, false);