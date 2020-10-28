const setElementListener = (elementList) => {
    for (let i = 0; i < elementList.length; i++) {
        elementList[i].addEventListener("click", function () {
            const postId = this.getElementsByTagName('h2')[0].getAttribute('id');
            const node = this;
            fetch(`/delete/${postId}`)
                .then(res => res.json())
                .then(res => {
                    if (res.status === 1) {
                        node.parentNode.removeChild(node);
                        console.log(res)
                    }
                    location.reload();
                })
                .catch(err => console.error(err));
    })
}};

const postElements = document.getElementsByClassName('entry');

console.log('Ok');
setElementListener(postElements);
