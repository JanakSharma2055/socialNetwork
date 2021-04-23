console.log("hello from index")

document.querySelectorAll(".edit").forEach((btn) => {
    let val = btn.dataset.id;
    btn.addEventListener("click", (event) => {
        let post_element = document.getElementById(val)
        btn.disabled = true
        post_element.innerHTML = `
        <form id="edit_post" class="card-text" style="margin-top: 1rem; margin-bottom: 1.6rem">
                    <div class="form-group" style="margin-bottom: .7rem">
                        <textarea 
                            id="edit_post_content">${post_element.innerHTML}
                        </textarea>
                    </div>
                    <input id="post-submit" type="submit" class="btn btn-primary " value="save"/>
                </form>
        `

        document.querySelector("#post-submit").addEventListener("click", (event) => {
            event.preventDefault()
            let post_Content = document.querySelector("#edit_post_content").value
            fetch('/edit', {
                method: 'POST',
                body: JSON.stringify({ post_Content, val })
            })
            .then(response => response.json())
                    .then(result => {
                        if (result.error) {
                            console.log(`Error: post is unable to change`);
                        } else {

                            console.log(result)
                            post_element.innerHTML=post_Content
                        }
                    })
                    .catch(err => {
                        console.log(err)
                    })




        })


    })
})