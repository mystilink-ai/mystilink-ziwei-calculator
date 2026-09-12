#!/usr/bin/env node
'use strict';

const path = require('path');
const { createClient } = require(path.join(__dirname, '../../bindings/js'));

async function main() {
  const client = createClient();
  const chart = await client.chart({
    datetime: '1990-05-15 14:30',
    timezone: 'Asia/Shanghai',
    gender: 'male',
    midnightZi: 'same-day',
    siHua: true,
    year: 2026,
    longitude: 121.5,
  });
  console.log(`ming=${chart.ming_gong_branch} frame=${chart.five_element_frame}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
