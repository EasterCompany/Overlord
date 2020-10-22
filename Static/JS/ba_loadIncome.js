function ba_loadIncome(){
    /* set income tab style */
    const tab = document.getElementById('income-tab');
    tab.style.backgroundColor = '#F77205';
    tab.style.boxShadow = '10px 10px 10px rgba(1,1,1,.8)';
    tab.style.color = 'white';
    /* set expense tab style */
    const otherTab = document.getElementById('expense-tab');
    otherTab.style.backgroundColor = 'unset';
    otherTab.style.boxShadow = '0 0 0 rgba(1,1,1,.8)';
    otherTab.style.color = 'grey';
    /* toggle content */
    const esec = document.getElementById('expenses');
    const isec = document.getElementById('incomes');
    esec.style.display = 'none';
    isec.style.display = 'block';
}