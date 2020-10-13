'use strict';

function getQuery(key) {
    return new URL(window.location.href).searchParams.get(key);
}
