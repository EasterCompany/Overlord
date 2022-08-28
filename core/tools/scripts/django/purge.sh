# Set working directory
cd ~/Easter/Dev/Ext/Overlord

# Output Script Header
echo
echo "   [PURGE GIT HISTORY SCRIPT]   "
echo
echo " [WARNING] -------------------- "
echo "  This will purge the local db  "
echo "  and all migration files for   "
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
    echo " >> Delete database"
    rm -rf db.sqlite3 &>> ~/.scripts.log
    echo "    Deleted successfully."
    echo

    echo
    echo " >> Delete API migrations"
    echo "      Deleting /api/migrations ..."
    rm api/migrations/0* &>> ~/.scripts.log
    rm api/migrations/1* &>> ~/.scripts.log
    rm api/migrations/2* &>> ~/.scripts.log
    rm api/migrations/3* &>> ~/.scripts.log
    rm api/migrations/4* &>> ~/.scripts.log
    rm api/migrations/5* &>> ~/.scripts.log
    rm api/migrations/6* &>> ~/.scripts.log
    rm api/migrations/7* &>> ~/.scripts.log
    rm api/migrations/8* &>> ~/.scripts.log
    rm api/migrations/9* &>> ~/.scripts.log
    echo "    Deleted successfully."
    echo

    echo
    echo " ----------------------------- "
    echo "   [ SCRIPT SUCCESSFULL ✔️]      "
    echo
fi
