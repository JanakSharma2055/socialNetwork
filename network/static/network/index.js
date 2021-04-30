console.log("hello from index")


document.querySelectorAll(".like").forEach((btn) => {
    
    let value = btn.dataset.id;
    btn.addEventListener("click", (event) => {
        console.log("clicked:" + value)
        fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({change_like: true, val: value})
        })
         .then(response => response.json())
         .then(result => {
             if (result.error) {
                 console.log(`Error liking post: ${result.error}`);
             } else {
                //  console.log("changed likedsds")
                console.log(result)

                 let likes_count = parseInt(document.querySelector(`#likes-${value}`).innerHTML)
                 let result_count=result.total_likes
                 console.log(likes_count)
                 console.log(result_count)
                 if(result_count<likes_count){
                     document.querySelector(`#likes-${value}`).innerHTML=result_count
                     btn.innerHTML = "<div style='color: rgb(235, 37, 70);'><i class=' far fa-heart fa-2x'></i></div>"

                 }
                 else if(result_count>likes_count){
                    document.querySelector(`#likes-${value}`).innerHTML=result_count
                    btn.innerHTML = "<div style='color: rgb(235, 37, 70);'><i class=' fas fa-heart fa-2x'></i></div>"
                    

                 }

                //  if (parseInt(result.likes_num) < parseInt(likes_count.innerHTML)) {
                //      btn.innerHTML = "<i class='mr-2 far fa-thumbs-up'></i>Like"
                //  } else if (parseInt(result.likes_num) > parseInt(likes_count.innerHTML)) {
                //      btn.innerHTML = "<div style='color: rgb(32, 120, 244);'><i class='mr-2 fas fa-thumbs-up'></i>Unlike</div>"
                //  }
                //  document.querySelector(`#likes${btn.dataset.postid}`).innerHTML = result.likes_num
             }
         })


    }
    )
}
)

document.querySelectorAll(".edit").forEach((btn) => {
    let val = btn.dataset.id;
    btn.addEventListener("click", (event) => {
        let post_element = document.getElementById(val)
        console.log(post_element)
        btn.disabled = true
        post_element.innerHTML = `
        <form id="edit_post" class="card-text" >
                    <div class="form-outline " >
                        <textarea class="form-control w-75" rows="2"
                            id="edit_post_content">${post_element.innerHTML}
                        </textarea>
                    </div>
                    <input id="post-submit" type="submit" class="btn btn-secondary " value="save"/>
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
                        post_element.innerHTML = post_Content
                    }
                })
                .catch(err => {
                    console.log(err)
                })




        })


    })
})



  