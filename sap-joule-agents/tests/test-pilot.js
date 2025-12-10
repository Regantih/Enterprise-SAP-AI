const getSupplierData = require('../skills/procurement/get-supplier-data');
const generateStrategy = require('../skills/procurement/generate-strategy');

async function runTests() {
    console.log("🧪 Starting Pilot Agent Tests...\n");

    // Test 1: Get Supplier Data
    console.log("Test 1: Fetching Supplier Data...");
    const supplierEvent = { data: { supplierId: "1000123" } };
    const supplierResult = await getSupplierData.handler(supplierEvent);

    if (supplierResult.status === 200 && supplierResult.data.name === "Acme Corp") {
        console.log("✅ GetSupplierData Passed");
    } else {
        console.error("❌ GetSupplierData Failed", supplierResult);
    }

    // Test 2: Generate Strategy
    console.log("\nTest 2: Generating Negotiation Strategy...");
    const strategyEvent = {
        data: {
            supplierData: supplierResult.data,
            marketData: { trend: "Stable" },
            objectives: ["Reduce price", "Maintain quality"]
        }
    };
    const strategyResult = await generateStrategy.handler(strategyEvent);

    if (strategyResult.status === 200 && strategyResult.data.strategy) {
        console.log("✅ GenerateStrategy Passed");
        console.log("\n--- Generated Strategy ---");
        console.log(strategyResult.data.strategy);
        console.log("--------------------------\n");
    } else {
        console.error("❌ GenerateStrategy Failed", strategyResult);
    }
}

runTests();
