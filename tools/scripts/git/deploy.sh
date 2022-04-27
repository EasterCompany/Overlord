# Set working directory
cd ~/Easter/Dev/Ext/Overlord

# Output Script Header
echo
echo "     [DEPLOY BRANCH SCRIPT]     "
echo
echo " [WARNING] -------------------- "
echo "  This will purge the git       "
echo "  history of the main branch on "
echo "  this repository.              "
echo
read -p "  Continue anyway (Y/N): " -n 1 -r > ~/.scripts.log
echo
echo " ------------------------------ "
echo

# Get User Confirmation
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo
    echo " >> Pull latest commits"
    git pull --recurse-submodules &>> ~/.scripts.log
    echo "    Pulled successfully."
    echo

    echo
    echo " >> Preserve content within a new branch"
    git checkout --orphan Orphan-Branch-Reserved-For-Dev-Ext-Overlord-Deployment &>> ~/.scripts.log
    echo "    Preserved successfully."
    echo

    echo
    echo " >> Make intial commit"
    echo "      adding everything to commit ..."
    git add .
    echo "      making commit with message ..."
    git commit -m "✨ [STABLE] Production $1" &>> ~/.scripts.log
    echo "    Made successfully."
    echo

    echo
    echo " >> Delete 'main' branch"
    git branch -D main &>> ~/.scripts.log
    echo "    Deleted successfully."
    echo

    echo
    echo " >> Create new 'main' branch"
    git branch -m main &>> ~/.scripts.log
    echo "    Created successfully."
    echo

    echo
    echo " >> Push ver. $1 initial commit "
    git push -f origin main &>> ~/.scripts.log
    echo "    Pushed successfully."
    echo

    echo
    echo " >> Delete branch & commit history"
    git gc --aggressive --prune=all &>> ~/.scripts.log
    echo "    Deleted successfully."
    echo

    echo
    echo " ----------------------------- "
    echo "   [ SCRIPT SUCCESSFULL ✔️]      "
    echo
fi
