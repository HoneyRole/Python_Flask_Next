function autoReloadOnServerChange() {
    fetch('/last_static_update').then(data => data.json()).then(result => {
        // initialize
        const max_age = Number(result.max_age);
        const rand_check_number = Number(result.rand_check_number);
        setInterval(_ => {
            fetch(
                `/last_static_update?max_age=${max_age}&rand_check_number=${rand_check_number}`, {
                    cache: "no-cache",
                }
            ).then(data => data.json()).then(result => {
                if (Number(result.max_age) > max_age || result.rand_check_number !== rand_check_number) {
                    window.location.reload();
                }
            })

        }, 15000);
    });
}

// auto refresh on static or app reload
autoReloadOnServerChange();
