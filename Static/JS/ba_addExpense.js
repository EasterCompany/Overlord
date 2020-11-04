let ba_expenseRowId = 0;
function ba_addExpense() {
    const div = document.getElementById(`expenses`);

    const desc = document.getElementById(`expense_desc`).value;
    if (desc.length === 0) {
        return alert('You must describe your expense.');
    };

    const cost = parseFloat(document.getElementById(`expense_cost`).value).toFixed(2);
    if (cost === 'NaN') {
        return alert('You must enter a cost value for your expense.');
    };

    const occr = document.getElementById(`expense_occr`).value;
    const cat = document.getElementById(`expense_cat`).value;

    div.innerHTML += `
    <div class='grid-row' id='expenseRow${ba_expenseRowId}'>
        <div class='grid-cell' id='${ba_expenseRowId}_desc'></div>
        <div class='grid-cell' id='${ba_expenseRowId}_cost'></div>
        <div class='grid-cell' id='${ba_expenseRowId}_occr'></div>
        <div class='grid-cell' id='${ba_expenseRowId}_cat'></div>
        <div class='grid-row-delete' id='${ba_expenseRowId}_delete'>
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
            width="24px" height="24px" viewBox="0 0 612 612" style="enable-background:new 0 0 612 612;" xml:space="preserve">
            <g><polygon points="612,36.004 576.521,0.603 306,270.608 35.478,0.603 0,36.004 270.522,306.011 0,575.997 35.478,611.397
            306,341.411 576.521,611.397 612,575.997 341.459,306.011"/></g></svg>
        </div>
    </div>`;

    const desc_div = document.getElementById(`${ba_expenseRowId}_desc`);
    const cost_div = document.getElementById(`${ba_expenseRowId}_cost`);
    const occr_div = document.getElementById(`${ba_expenseRowId}_occr`);
    const cat_div = document.getElementById(`${ba_expenseRowId}_cat`);

    desc_div.innerText = desc;
    cost_div.innerText = cost;
    occr_div.innerText = occr;
    cat_div.innerText = cat;

    ba_expenseRowId += 1;
};