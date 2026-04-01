document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("productCreateForm");

    if (form) {
        form.addEventListener("submit", async function (e) {
            // 1. 가장 중요: 브라우저의 기본 GET 전송을 무조건 막습니다.
            e.preventDefault();
            e.stopPropagation(); 

            const formData = new FormData();
            formData.append("name", document.getElementById("name").value);
            formData.append("description", document.getElementById("description").value);
            formData.append("price", document.getElementById("price").value);
            
            const imageFile = document.getElementById("image").files[0];
            if (imageFile) {
                formData.append("image", imageFile);
            }

            try {
                // 2. POST로 데이터를 보냅니다.
                const response = await axios.post("/products/api/", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                alert("상품이 등록되었습니다!");
                window.location.href = "/products/"; // 등록 후 목록으로 이동
            } catch (error) {
                console.error("등록 실패:", error.response?.data);
                alert("등록 실패: " + JSON.stringify(error.response?.data));
            }
        });
    }
});