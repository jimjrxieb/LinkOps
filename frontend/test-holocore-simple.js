#!/usr/bin/env node

/**
 * HoloCore Simple Integration Test
 * Tests backend API endpoints using fetch
 */

const API_BASE = 'http://localhost:8000';

const testCases = [
  {
    name: 'Backend Health Check',
    test: async () => {
      const response = await fetch(`${API_BASE}/health`);
      return response.status === 200;
    }
  },
  {
    name: 'James Task Evaluation',
    test: async () => {
      const taskData = {
        task_id: 'test/holocore-integration',
        task_description: 'Test HoloCore integration with Vue frontend'
      };
      const response = await fetch(`${API_BASE}/api/james/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData)
      });
      const data = await response.json();
      return data && data.detected_category;
    }
  },
  {
    name: 'Whis Queue Status',
    test: async () => {
      const response = await fetch(`${API_BASE}/api/whis/queue`);
      const data = await response.json();
      return data && typeof data.pending === 'number';
    }
  },
  {
    name: 'Whis Approvals',
    test: async () => {
      const response = await fetch(`${API_BASE}/api/whis/approvals`);
      const data = await response.json();
      return Array.isArray(data);
    }
  },
  {
    name: 'Whis Digest',
    test: async () => {
      const response = await fetch(`${API_BASE}/api/whis/digest`);
      const data = await response.json();
      return data && data.runes_created !== undefined;
    }
  }
];

async function runTests() {
  console.log('🧠 HoloCore Integration Test');
  console.log('=' .repeat(50));
  console.log(`Testing Backend: ${API_BASE}`);
  console.log('');

  let passed = 0;
  let failed = 0;

  for (const testCase of testCases) {
    try {
      console.log(`Testing: ${testCase.name}...`);
      const result = await testCase.test();
      
      if (result) {
        console.log(`✅ ${testCase.name} - PASSED`);
        passed++;
      } else {
        console.log(`❌ ${testCase.name} - FAILED`);
        failed++;
      }
    } catch (error) {
      console.log(`❌ ${testCase.name} - ERROR: ${error.message}`);
      failed++;
    }
    console.log('');
  }

  console.log('=' .repeat(50));
  console.log(`Results: ${passed} passed, ${failed} failed`);
  
  if (failed === 0) {
    console.log('🎉 All tests passed! HoloCore is ready.');
    console.log('');
    console.log('Next steps:');
    console.log('1. Start frontend: cd frontend && npm run dev');
    console.log('2. Visit: http://localhost:3000');
    console.log('3. Command your AI army!');
  } else {
    console.log('⚠️  Some tests failed. Check backend status.');
  }
}

// Check if backend is running
async function checkBackend() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    return response.status === 200;
  } catch (error) {
    console.log('❌ Backend not running. Start with: cd core && docker-compose up -d');
    return false;
  }
}

async function main() {
  const backendRunning = await checkBackend();
  if (backendRunning) {
    await runTests();
  }
}

main().catch(console.error); 