#!/usr/bin/env node

/**
 * HoloCore Integration Test
 * Tests all Vue frontend + backend API integration
 */

import axios from 'axios';

const API_BASE = 'http://localhost:8000';
const FRONTEND_URL = 'http://localhost:3000';

const testCases = [
  {
    name: 'Backend Health Check',
    test: async () => {
      const response = await axios.get(`${API_BASE}/health`);
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
      const response = await axios.post(`${API_BASE}/api/james/evaluate`, taskData);
      return response.data && response.data.detected_category;
    }
  },
  {
    name: 'Whis Queue Status',
    test: async () => {
      const response = await axios.get(`${API_BASE}/api/whis/queue`);
      return response.data && typeof response.data.pending === 'number';
    }
  },
  {
    name: 'Whis Approvals',
    test: async () => {
      const response = await axios.get(`${API_BASE}/api/whis/approvals`);
      return Array.isArray(response.data);
    }
  },
  {
    name: 'Whis Digest',
    test: async () => {
      const response = await axios.get(`${API_BASE}/api/whis/digest`);
      return response.data && response.data.runes_created !== undefined;
    }
  },
  {
    name: 'Night Training',
    test: async () => {
      const response = await axios.post(`${API_BASE}/api/whis/train-nightly`);
      return response.data && response.data.tasks_processed !== undefined;
    }
  }
];

async function runTests() {
  console.log('🧠 HoloCore Integration Test');
  console.log('=' .repeat(50));
  console.log(`Testing Backend: ${API_BASE}`);
  console.log(`Frontend URL: ${FRONTEND_URL}`);
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
    console.log('1. Start frontend: npm run dev');
    console.log('2. Visit: http://localhost:3000');
    console.log('3. Command your AI army!');
  } else {
    console.log('⚠️  Some tests failed. Check backend status.');
  }
}

// Check if backend is running
async function checkBackend() {
  try {
    await axios.get(`${API_BASE}/health`);
    return true;
  } catch (error) {
    console.log('❌ Backend not running. Start with: cd ../core && docker-compose up -d');
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