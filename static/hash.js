const bcrypt = require('bcrypt');
const saltRounds = 10;
const yourPassword = "someRandomPasswordHere";

bcrypt.hash(, saltRounds, (err, hash) => {
    // Now we can store the password hash in db.
});

function hashPass() {
    let password = document.getElementById("inputPassword5");
    let passwordText = password.nodeValue;
    bcrypt.hash(password, saltRounds, (err, hash) => {
        // Now we can store the password hash in db.
    });
}