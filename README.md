# Save coupons
Save coupons automatically!

## Suggestions
Tired of receipts longer than the toilet paper you just bought?

If you want more coupons and want to save the environment at the same time, I highly suggest signing up to [digital receipts](https://www.cvs.com/content/digital-receipt "CVS Digital Receipts") or [registering an account](https://www.walgreens.com/register/regOptions.jsp "Walgreens Accounts")!

By doing so, the coupons that typically print on your receipt will instead be sent to your email; from there you'll be able to send these coupons directly to your card. Once they're on your card, they'll be applied automatically when you check out—no need to remember to bring them to the store and apply them yourself anymore!

## Installation
This script has a few dependencies that must be installed before use.

### Chromedriver
The easiest way to install this is with Homebrew. In a command line window, run `brew cask install chromedriver` and it will be automatically installed.

If you do not have Homebrew installed, follow the instructions on [its website](https://brew.sh/ "Homebrew").

### Splinter
To install the splinter library to Python, use pip by running `sudo pip install splinter`. You may have to enter your password.

## Use and Debugging
### <a name="use"></a>Running the Script
1. In a Terminal window, navigate to the folder in which the Python file is located (using `cd`).
2. Then, run the bash script with `./save_money.sh`. This script will automatically update your local repo with the latest code and start the Python script.
3. Follow the prompts.
4. Save money at the store!

### Debugging
If the bash script does not work, it may have failed on some intermediate step, or it might not have permissions to run.

If the issue is permissions:

1. Run `chmod u+x save_money.sh`
2. Try to run it again with the steps in [Running the Script](#use) above.

If the script fails on an intermediate step, run the steps manually to diagnose the issue:

1. Update the local repo with `git pull`.
2. Run the Python script with `python coupons.py`.
