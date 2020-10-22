function ba_loadExpense(){
    /* set expense tab style */
    const tab = document.getElementById('expense-tab');
    tab.style.backgroundColor = '#F77205';
    tab.style.boxShadow = '10px 10px 10px rgba(1,1,1,.8)';
    tab.style.color = 'white';
    /* set income tab style */
    const otherTab = document.getElementById('income-tab');
    otherTab.style.backgroundColor = 'unset';
    otherTab.style.boxShadow = '0 0 0 rgba(1,1,1,.8)';
    otherTab.style.color = 'grey';
    /* toggle content */
    const esec = document.getElementById('expenses');
    const isec = document.getElementById('incomes');
    esec.style.display = 'block';
    isec.style.display = 'none';
}