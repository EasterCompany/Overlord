# Set working directory
cd ~/Easter/Dev/Ext/Overlord
# Output Script Header
echo
echo "       UPDATE REPOSITORIES      "
echo " ------------------------------ "
echo

# Add Files, Commit & Push 'Overlord'
echo
echo " >> Overlord "
cd ~/Easter/Dev/Ext/Overlord
echo "      branch:             main "
git checkout main &> ~/.scripts.log
echo "      pulling files        ... "
git pull origin main --recurse-submodules &>> ~/.scripts.log
echo "    Success                 ✔️ "
echo

if [ -d "clients/__react__" ]
then
    # Add Files, Commit & Push 'Overlord-React'
    echo
    echo " >> Overlord-React "
    cd ~/Easter/Dev/Ext/Overlord/clients/__react__
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      pulling files        ... "
    git pull origin main --recurse-submodules &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    echo
fi

if [ -d "clients/__angular__" ]
then
    # Add Files, Commit & Push 'Overlord-React'
    echo
    echo " >> Overlord-Angular "
    cd ~/Easter/Dev/Ext/Overlord/clients/__angular__
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      pulling files        ... "
    git pull origin main --recurse-submodules &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    echo
fi

if [ -d "clients/pardoewray" ]
then
    # Add Files, Commit & Push '@Ext/Pardoewray'
    echo
    echo " >> Pardoewray "
    cd ~/Easter/Dev/Ext/Overlord/clients/pardoewray
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      pulling files        ... "
    git pull origin main --recurse-submodules &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    echo
fi

if [ -d "clients/inverair" ]
then
    # Add Files, Commit & Push '@Ext/Pardoewray'
    echo
    echo " >> Inverair "
    cd ~/Easter/Dev/Ext/Overlord/clients/inverair
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      pulling files        ... "
    git pull origin main --recurse-submodules &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    echo
fi

echo
echo " ------------------------------ "
echo " [ SUCCESSFULLY UPDATED REPOS ] "
echo
