const axios = require("axios");
const fs = require("fs");
const path = require("path");
const os = require("os");
const ProgressBar = require("progress");

// 啟動時接受 URL 參數
const args = process.argv.slice(2);
const url = args[0];

if (!url) {
  console.error('Provide URL in the args！');
  console.error('Instruction：node downloadPDF.js <URL>');
  process.exit(1);
}

// PDF 檔案的 URL
// const url =
//   "https://ncstatic.clewm.net/rsrc/2024/0709/20/6621744d928ff70a25f9c7150600a436.pdf";

// 本地儲存檔案名稱
const timestamp = new Date().getTime();
const downloadsDir = path.join(os.homedir(), "Downloads");
const outputFileName = path.join(downloadsDir, `${timestamp}.pdf`);

async function downloadPDF() {
  try {
    console.log("Initializing...");

    // 發送 HEAD 請求以獲取檔案大小
    const headResponse = await axios.head(url);
    const totalSize = parseInt(headResponse.headers["content-length"], 10);

    console.log(`File size: ${(totalSize / (1024 * 1024)).toFixed(2)} MB`);

    // 初始化進度條
    const progressBar = new ProgressBar("Downloading [:bar] :percent :etas", {
      width: 40,
      complete: "=",
      incomplete: " ",
      total: totalSize,
    });

    // 發送 GET 請求下載 PDF
    const response = await axios({
      url: url,
      method: "GET",
      responseType: "stream",
    });

    // 建立寫入檔案的資料流
    const writer = fs.createWriteStream(outputFileName);

    // 監聽資料流進度
    response.data.on("data", (chunk) => {
      progressBar.tick(chunk.length);
    });

    // 將資料流寫入本地檔案
    response.data.pipe(writer);

    // 完成後的事件處理
    writer.on("finish", () => {
      console.log(`PDF Download successfully: ${outputFileName}`);
    });

    writer.on("error", (err) => {
      console.error("Error occurred while writing file:", err);
    });
  } catch (error) {
    console.error("Error occurred while downloading file:", error.message);
  }
}

// 執行下載函式
downloadPDF();
