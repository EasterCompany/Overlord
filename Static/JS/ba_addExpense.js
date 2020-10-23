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
    <div id='expenseRow` + String(ba_expenseRowId) + `' style='border-bottom:1px solid grey;padding:3px 3px 3px 3px;display:flex;'>
        <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>` + desc + `</div>
        <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>` + cost + `</div>
        <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>` + occr + `</div>
        <div style='border-right:1px solid grey;width:25%;padding-top:6px;overflow:hidden;font-size:.8rem;'>` + cat + `</div>
        <div style='width:20px;height:20px;padding:4px 4px 4px 4px;'>
        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        width="24px" height="24px" viewBox="0 0 612 612" style="enable-background:new 0 0 612 612;" xml:space="preserve">
        <g><polygon points="612,36.004 576.521,0.603 306,270.608 35.478,0.603 0,36.004 270.522,306.011 0,575.997 35.478,611.397 
        306,341.411 576.521,611.397 612,575.997 341.459,306.011"/></g></svg>
        </div>
    </div>`;
    ba_expenseRowId += 1;
};