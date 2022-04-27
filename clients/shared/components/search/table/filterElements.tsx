
const filterElements = (searchBoxId: string, elementsListLength: number) => {
  const searchBox = document.querySelector(`#${searchBoxId}`) as HTMLInputElement;

  for (let i=0; i < elementsListLength; i++) {
    const index = document.getElementById(`${i}`) as HTMLInputElement;
    const indexText = index.innerText.toLowerCase().replace(/\s/g, '');
    const searchText = searchBox.value.toLowerCase().replace(/\s/g, '');

    if (indexText.includes(searchText)) index.style.display = "";
    else index.style.display = "none";
  }
}


export default filterElements;
