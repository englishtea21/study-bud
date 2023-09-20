// infinite pagination
const fetchPage = async (url) => {
    return fetch(url,
        {
            method: 'GET',
            credentials: 'same-origin',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                // "X-CSRFToken": getCookie("csrftoken"),
                // "X-CSRFToken": csrftoken,
                "Accept": "application/json",
                'Content-Type': 'text/html',
            },
        }
    )
}

// Infinite Pagination

class InfinitePagination {
    #scrollElement;
    #sentinel;
    #subdomain;
    #observer;
    #end;
    #counter;
    #pageQueryName;

    constructor(scrollElement, subdomain, pageQueryName, sentinelId) {
        this.#scrollElement = scrollElement;

        this.#subdomain = subdomain;

        this.#pageQueryName = pageQueryName;

        this.#sentinel = document.createElement('div');
        this.#sentinel.id = sentinelId;

        this.#scrollElement.parentNode.insertBefore(this.#sentinel, this.#scrollElement.nextSibling);

        this.#end = false;
        this.#counter = 2;

        this.#observer = new IntersectionObserver(async (entries) => {
            let entry = entries[0];
            if (entry.intersectionRatio > 0 && !this.#end) {
                let url = `${this.#subdomain}/?${this.#pageQueryName}=${this.#counter}`;
                let req = await fetchPage(url);
                if (req.ok) {
                    let body = await req.text();
                    // Be careful of XSS if you do this. Make sure
                    // you remove all possible sources of XSS.
                    // console.log(body)
                    this.#counter++;

                    this.#scrollElement.innerHTML += body;

                } else {
                    // If it returns a 404, stop requesting new items
                    this.#end = true;
                }
            }
        });
        this.#observer.observe(this.#sentinel);
    }

    stopPagination() {
        this.#observer.disconnect();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // feed pagination
    let feedScrollElement = document.getElementById("feed-infinite-container");
    let feedInfinitePagination = new InfinitePagination(feedScrollElement, pageQueryName='page', subdomain = '', sentinelId = 'feed-sentinel');


    // activities pagination
    let activitiesScrollElement = document.getElementById('activities-infinite-container');
    let activitiesInfinitePagination = new InfinitePagination(activitiesScrollElement, pageQueryName='activitiesPage', subdomain = '', sentinelId = 'activities-sentinel');
})