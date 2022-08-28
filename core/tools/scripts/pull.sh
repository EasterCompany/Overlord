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

if [ -d "clients/pardoewray" ]
then
    # Add Files, Commit & Push '@Ext/PardoeWray'
    echo
    echo " >> Pardoewray "
    cd ~/Easter/Dev/Ext/Overlord/clients/pardoewray
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      pulling files        ... "
    git pull origin main --recurse-submodules &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    cd ~/Easter/Dev/Ext/Overlord
    echo
fi

if [ -d "clients/inverair" ]
then
    # Add Files, Commit & Push '@Ext/InverAir'
    echo
    echo " >> Inverair "
    cd ~/Easter/Dev/Ext/Overlord/clients/inverair
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      pulling files        ... "
    git pull origin main --recurse-submodules &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    cd ~/Easter/Dev/Ext/Overlord
    echo
fi

echo
echo " ------------------------------ "
echo " [ SUCCESSFULLY UPDATED REPOS ] "
echo
