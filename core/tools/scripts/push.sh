# Set working directory
cd ~/Easter/Dev/Ext/Overlord
DATE=`date '+%d/%B/%Y'`
AUTO_MESSAGE="🤖 [COMMIT] $DATE $@"
FIX_MESSAGE="🔧 [HOTFIX] $DATE $@"

# Output Script Header
echo
echo "    [GIT AUTO COMMIT SCRIPT]    "
echo " ------------------------------ "
echo

# Add Files, Commit & Push 'Overlord'
echo
echo " >> Overlord "
cd ~/Easter/Dev/Ext/Overlord
echo "      branch:             main "
git checkout main &> ~/.scripts.log
echo "      adding files         ... "
git add . &>> ~/.scripts.log
echo "      making commit        ... "
git commit -m "$AUTO_MESSAGE" &>> ~/.scripts.log
echo "      Pushing              ... "
git push origin main &>> ~/.scripts.log
echo "    Success                 ✔️ "
echo

if [ -d "clients/pardoewray" ]
then
    # Add Files, Commit & Push '@Ext/Pardoewray'
    echo
    echo " >> Pardoewray "
    cd ~/Easter/Dev/Ext/Overlord/clients/pardoewray
    echo "      branch:             main "
    git checkout main &> ~/.scripts.log
    echo "      adding files         ... "
    git add . &>> ~/.scripts.log
    echo "      making commit        ... "
    git commit -m "$AUTO_MESSAGE" &>> ~/.scripts.log
    echo "      Pushing              ... "
    git push origin main &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    cd ~/Easter/Dev/Ext/Overlord
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
    echo "      adding files         ... "
    git add . &>> ~/.scripts.log
    echo "      making commit        ... "
    git commit -m "$AUTO_MESSAGE" &>> ~/.scripts.log
    echo "      Pushing              ... "
    git push origin main &>> ~/.scripts.log
    echo "    Success                 ✔️ "
    cd ~/Easter/Dev/Ext/Overlord
    echo
fi

# Finalize
echo
echo " >> $AUTO_MESSAGE"
cd ~/Easter/Dev/Ext/Overlord
git add . &>> ~/.scripts.log
git commit -m "..." &>> ~/.scripts.log
git push origin main &>> ~/.scripts.log
echo "    Finalized               ✔️ "
echo

echo
echo " ------------------------------ "
echo "  [ SUCCESSFULLY AUTO COMMIT ]  "
echo
