// API基础URL
const API_BASE = '/api';

// 全局状态
let allIntelligence = [];
let currentEditingId = null;
let currentView = 'timeline';
let currentTab = 'all';
let autoScrollEnabled = true;
let displayedCount = 20;
let tickerInterval = null;

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
    loadIntelligence();
    setupFormSubmit();
    initTicker();
    
    // 自动刷新（每30秒）
    setInterval(loadIntelligence, 30000);
});

// 加载情报列表
async function loadIntelligence() {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE}/intelligence?limit=100`);
        if (response.ok) {
            allIntelligence = await response.json();
            updateStatistics();
            displayIntelligence(allIntelligence);
        } else {
            showNotification('加载数据失败', 'error');
        }
    } catch (error) {
        console.error('Error loading intelligence:', error);
        showNotification('网络错误，请检查服务是否运行', 'error');
    } finally {
        showLoading(false);
    }
}

// 显示情报列表
function displayIntelligence(intelligenceList) {
    const container = document.getElementById('intelligenceList');
    const emptyState = document.getElementById('emptyState');
    const loadMoreContainer = document.getElementById('loadMoreContainer');
    
    if (intelligenceList.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        loadMoreContainer.style.display = 'none';
        return;
    }
    
    emptyState.style.display = 'none';
    
    // 根据当前视图显示
    const viewClass = currentView === 'grid' ? 'grid-view' : 'timeline-view';
    container.className = `intelligence-list ${viewClass}`;
    
    // 限制显示数量
    const displayList = intelligenceList.slice(0, displayedCount);
    container.innerHTML = displayList.map(item => createIntelligenceCard(item)).join('');
    
    // 显示加载更多按钮
    if (intelligenceList.length > displayedCount) {
        loadMoreContainer.style.display = 'block';
    } else {
        loadMoreContainer.style.display = 'none';
    }
    
    // 更新快讯流
    updateTicker(intelligenceList.filter(item => item.rating >= 4));
    
    // 更新主要文章
    updateFeaturedArticle(intelligenceList);
    
    // 更新最新快讯列表
    updateLatestNews(intelligenceList);
    
    // 更新链上监控
    updateChainMonitor(intelligenceList.filter(item => item.rating >= 4));
    
    // 更新右侧快讯列表
    updateRightNewsList(intelligenceList.slice(0, 10));
    
    // 更新热门情报
    updateHotIntelligence(intelligenceList);
    
    // 更新融资动向
    updateFundingList(intelligenceList);
}

// 创建情报卡片HTML
function createIntelligenceCard(item) {
    const rating = item.rating || 0;
    const stars = '⭐'.repeat(rating);
    const ratingClass = `rating-${rating}`;
    const statusClass = item.status || 'pending';
    const createdDate = item.created_at ? new Date(item.created_at).toLocaleString('zh-CN') : '未知';
    const timeAgo = getTimeAgo(item.created_at);
    const itemClass = currentView === 'timeline' ? 'timeline-item' : 'grid-item';
    
    // 判断标签
    const tags = [];
    if (rating >= 4) tags.push('<span class="tag hot">热门</span>');
    if (isNew(item.created_at)) tags.push('<span class="tag new">最新</span>');
    if (rating === 5) tags.push('<span class="tag urgent">紧急</span>');
    
    return `
        <div class="intelligence-card ${ratingClass} ${itemClass}">
            <div class="card-header">
                <div style="flex: 1;">
                    <div class="card-title">
                        ${escapeHtml(item.title)}
                        ${tags.join('')}
                    </div>
                    <div class="card-meta">
                        <span class="meta-item">
                            <i class="fas fa-star"></i>
                            <span class="rating-badge ${ratingClass}">${stars} ${rating}星</span>
                        </span>
                        <span class="meta-item">
                            <i class="fas fa-circle"></i>
                            <span class="status-badge ${statusClass}">${getStatusText(item.status)}</span>
                        </span>
                        <span class="meta-item">
                            <i class="fas fa-clock"></i>
                            ${timeAgo}
                        </span>
                        ${item.source ? `
                        <span class="meta-item">
                            <i class="fas fa-tag"></i>
                            ${escapeHtml(item.source)}
                        </span>
                        ` : ''}
                    </div>
                </div>
            </div>
            <div class="card-content">
                ${escapeHtml(item.content.substring(0, 200))}${item.content.length > 200 ? '...' : ''}
            </div>
            <div class="card-actions">
                ${item.status !== 'published' ? `
                <button class="btn btn-success btn-sm" onclick="pushIntelligence(${item.id})">
                    <i class="fas fa-paper-plane"></i> 推送
                </button>
                ` : ''}
                <button class="btn btn-primary btn-sm" onclick="editIntelligence(${item.id})">
                    <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn btn-secondary btn-sm" onclick="classifyIntelligence(${item.id})">
                    <i class="fas fa-star"></i> 分级
                </button>
            </div>
        </div>
    `;
}

// 更新统计信息
function updateStatistics() {
    const total = allIntelligence.length;
    const highRating = allIntelligence.filter(item => item.rating >= 4).length;
    const published = allIntelligence.filter(item => item.status === 'published').length;
    const pending = allIntelligence.filter(item => item.status === 'pending').length;
    
    document.getElementById('totalCount').textContent = total;
    document.getElementById('highRatingCount').textContent = highRating;
    document.getElementById('publishedCount').textContent = published;
    document.getElementById('pendingCount').textContent = pending;
}

// 筛选情报
function filterIntelligence() {
    const ratingFilter = document.getElementById('ratingFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    const searchText = document.getElementById('searchInput').value.toLowerCase();
    
    let filtered = [...allIntelligence];
    
    // 标签筛选
    if (currentTab === 'hot') {
        filtered = filtered.filter(item => item.rating >= 4);
    } else if (currentTab === 'latest') {
        filtered = filtered.sort((a, b) => {
            const timeA = new Date(a.created_at || 0).getTime();
            const timeB = new Date(b.created_at || 0).getTime();
            return timeB - timeA;
        });
    } else if (currentTab === 'high') {
        filtered = filtered.filter(item => item.rating >= 3);
    }
    
    if (ratingFilter) {
        filtered = filtered.filter(item => item.rating == ratingFilter);
    }
    
    if (statusFilter) {
        filtered = filtered.filter(item => item.status === statusFilter);
    }
    
    if (searchText) {
        filtered = filtered.filter(item => 
            item.title.toLowerCase().includes(searchText) ||
            item.content.toLowerCase().includes(searchText)
        );
    }
    
    displayIntelligence(filtered);
    displayedCount = 20; // 重置显示数量
}

// 标签筛选
function filterByTab(tab) {
    currentTab = tab;
    
    // 更新标签按钮状态
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tab) {
            btn.classList.add('active');
        }
    });
    
    filterIntelligence();
}

// 排序
function sortIntelligence() {
    const sortType = document.getElementById('sortSelect').value;
    let sorted = [...allIntelligence];
    
    if (sortType === 'time') {
        sorted.sort((a, b) => {
            const timeA = new Date(a.created_at || 0).getTime();
            const timeB = new Date(b.created_at || 0).getTime();
            return timeB - timeA;
        });
    } else if (sortType === 'rating') {
        sorted.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    } else if (sortType === 'hot') {
        sorted.sort((a, b) => {
            const scoreA = (a.rating || 0) * 10 + (a.status === 'published' ? 5 : 0);
            const scoreB = (b.rating || 0) * 10 + (b.status === 'published' ? 5 : 0);
            return scoreB - scoreA;
        });
    }
    
    allIntelligence = sorted;
    filterIntelligence();
}

// 视图切换
function switchView(view) {
    currentView = view;
    
    // 更新按钮状态
    document.getElementById('timelineViewBtn').classList.toggle('active', view === 'timeline');
    document.getElementById('gridViewBtn').classList.toggle('active', view === 'grid');
    
    // 重新显示
    filterIntelligence();
}

// 加载更多
function loadMore() {
    displayedCount += 20;
    filterIntelligence();
}

// 初始化快讯流
function initTicker() {
    if (autoScrollEnabled) {
        startTicker();
    }
}

// 更新快讯流
function updateTicker(highValueItems) {
    const tickerScroll = document.getElementById('tickerScroll');
    if (!tickerScroll) return;
    
    // 只显示4-5星的最新情报
    const tickerItems = highValueItems
        .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
        .slice(0, 10);
    
    if (tickerItems.length === 0) {
        tickerScroll.innerHTML = '<div class="ticker-item"><span>暂无高价值快讯</span></div>';
        return;
    }
    
    // 创建快讯项（重复一次以实现无缝滚动）
    const itemsHtml = tickerItems.map(item => {
        const timeAgo = getTimeAgo(item.created_at);
        const stars = '⭐'.repeat(item.rating || 0);
        return `
            <div class="ticker-item new">
                <div class="ticker-item-rating">${stars}</div>
                <div class="ticker-item-title">${escapeHtml(item.title)}</div>
                <div class="ticker-item-time">${timeAgo}</div>
            </div>
        `;
    }).join('');
    
    tickerScroll.innerHTML = itemsHtml + itemsHtml; // 重复以实现无缝滚动
}

// 切换自动滚动
function toggleAutoScroll() {
    autoScrollEnabled = !autoScrollEnabled;
    const btn = document.getElementById('autoScrollBtn');
    const tickerScroll = document.getElementById('tickerScroll');
    
    if (autoScrollEnabled) {
        btn.innerHTML = '<i class="fas fa-pause"></i>';
        tickerScroll.classList.remove('paused');
        startTicker();
    } else {
        btn.innerHTML = '<i class="fas fa-play"></i>';
        tickerScroll.classList.add('paused');
        stopTicker();
    }
}

function startTicker() {
    // 快讯流自动滚动已在CSS中实现
}

function stopTicker() {
    // 停止滚动
}

// 显示创建模态框
function showCreateModal() {
    currentEditingId = null;
    document.getElementById('modalTitle').textContent = '创建新情报';
    document.getElementById('intelligenceForm').reset();
    document.getElementById('createModal').classList.add('active');
}

// 关闭模态框
function closeModal() {
    document.getElementById('createModal').classList.remove('active');
    currentEditingId = null;
}

// 编辑情报
async function editIntelligence(id) {
    const item = allIntelligence.find(i => i.id === id);
    if (!item) return;
    
    currentEditingId = id;
    document.getElementById('modalTitle').textContent = '编辑情报';
    document.getElementById('intelligenceTitle').value = item.title;
    document.getElementById('intelligenceContent').value = item.content;
    document.getElementById('intelligenceSource').value = item.source || '';
    document.getElementById('intelligenceRating').value = item.rating || '';
    
    document.getElementById('createModal').classList.add('active');
}

// 分级情报
async function classifyIntelligence(id) {
    const rating = prompt('请输入评级 (1-5):');
    if (!rating || rating < 1 || rating > 5) {
        showNotification('评级必须是1-5之间的数字', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/intelligence/${id}/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rating: parseInt(rating) })
        });
        
        if (response.ok) {
            showNotification('分级成功', 'success');
            loadIntelligence();
        } else {
            showNotification('分级失败', 'error');
        }
    } catch (error) {
        console.error('Error classifying:', error);
        showNotification('网络错误', 'error');
    }
}

// 推送情报
async function pushIntelligence(id) {
    if (!confirm('确定要推送这条情报吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE}/push/${id}`, {
            method: 'POST'
        });
        
        if (response.ok) {
            showNotification('推送成功', 'success');
            loadIntelligence();
        } else {
            const error = await response.json();
            showNotification(error.error || '推送失败', 'error');
        }
    } catch (error) {
        console.error('Error pushing:', error);
        showNotification('网络错误', 'error');
    }
}

// 设置表单提交
function setupFormSubmit() {
    document.getElementById('intelligenceForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const data = {
            title: document.getElementById('intelligenceTitle').value,
            content: document.getElementById('intelligenceContent').value,
            source: document.getElementById('intelligenceSource').value || null,
            rating: document.getElementById('intelligenceRating').value ? 
                parseInt(document.getElementById('intelligenceRating').value) : null
        };
        
        try {
            let response;
            if (currentEditingId) {
                // 更新
                response = await fetch(`${API_BASE}/intelligence/${currentEditingId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
            } else {
                // 创建
                response = await fetch(`${API_BASE}/intelligence`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
            }
            
            if (response.ok) {
                const saved = await response.json();

                // 本地即时更新，避免等待下一次请求才显示
                if (currentEditingId) {
                    allIntelligence = allIntelligence.map(item =>
                        item.id === currentEditingId ? saved : item
                    );
                } else {
                    allIntelligence.unshift(saved);
                }

                updateStatistics();
                displayIntelligence(allIntelligence);

                showNotification(currentEditingId ? '更新成功' : '创建成功', 'success');
                closeModal();
                
                // 再拉一次后端数据，确保与服务器完全一致
                loadIntelligence();
            } else {
                const error = await response.json();
                showNotification(error.error || '操作失败', 'error');
            }
        } catch (error) {
            console.error('Error saving:', error);
            showNotification('网络错误', 'error');
        }
    });
}

// 刷新数据
function refreshData() {
    loadIntelligence();
    showNotification('数据已刷新', 'info');
}

// 显示/隐藏加载动画
function showLoading(show) {
    document.getElementById('loadingSpinner').style.display = show ? 'block' : 'none';
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// 工具函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function getStatusText(status) {
    const statusMap = {
        'pending': '待处理',
        'published': '已推送',
        'archived': '已归档'
    };
    return statusMap[status] || status;
}

// 获取相对时间
function getTimeAgo(dateString) {
    if (!dateString) return '未知';
    
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) return `${days}天前`;
    if (hours > 0) return `${hours}小时前`;
    if (minutes > 0) return `${minutes}分钟前`;
    return '刚刚';
}

// 判断是否为新情报（1小时内）
function isNew(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    return diff < 3600000; // 1小时
}

// 更新主要文章
function updateFeaturedArticle(intelligenceList) {
    const featuredContainer = document.getElementById('featuredArticle');
    if (!featuredContainer) return;
    
    // 选择最高评级的最新文章
    const featured = intelligenceList
        .sort((a, b) => {
            const ratingDiff = (b.rating || 0) - (a.rating || 0);
            if (ratingDiff !== 0) return ratingDiff;
            return new Date(b.created_at || 0) - new Date(a.created_at || 0);
        })[0];
    
    if (featured) {
        const timeAgo = getTimeAgo(featured.created_at);
        featuredContainer.innerHTML = `
            <div class="article-image">
                <i class="fas fa-newspaper" style="font-size: 64px; color: var(--accent-color); opacity: 0.3;"></i>
            </div>
            <div class="article-content">
                <div class="article-title">${escapeHtml(featured.title)}</div>
                <div class="article-meta">
                    <span><i class="fas fa-clock"></i> ${timeAgo}</span>
                    <span><i class="fas fa-star"></i> ${featured.rating || 0}星</span>
                    <span><i class="fas fa-tag"></i> ${featured.source || '未知来源'}</span>
                </div>
            </div>
        `;
    } else {
        featuredContainer.innerHTML = `
            <div class="article-content" style="text-align: center; padding: 40px;">
                <i class="fas fa-inbox" style="font-size: 48px; color: var(--text-muted); margin-bottom: 15px;"></i>
                <p style="color: var(--text-secondary);">暂无主要文章</p>
            </div>
        `;
    }
}

// 更新最新快讯列表
function updateLatestNews(intelligenceList) {
    const newsList = document.getElementById('latestNewsList');
    if (!newsList) return;
    
    const latest = intelligenceList
        .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
        .slice(0, 5);
    
    if (latest.length === 0) {
        newsList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px;">暂无快讯</p>';
        return;
    }
    
    newsList.innerHTML = latest.map(item => {
        const timeAgo = getTimeAgo(item.created_at);
        const rating = item.rating || 0;
        const tags = [];
        if (rating >= 4) tags.push(`<span class="news-tag">高价值</span>`);
        if (isNew(item.created_at)) tags.push(`<span class="news-tag">最新</span>`);
        
        return `
            <div class="news-item" onclick="viewIntelligence(${item.id})">
                <div class="news-item-title">${escapeHtml(item.title)}</div>
                <div class="news-item-meta">
                    <span><i class="fas fa-clock"></i> ${timeAgo}</span>
                    <span><i class="fas fa-star"></i> ${rating}星</span>
                </div>
                ${tags.length > 0 ? `<div class="news-item-tags">${tags.join('')}</div>` : ''}
            </div>
        `;
    }).join('');
}

// 更新链上监控
function updateChainMonitor(highValueItems) {
    const monitorList = document.getElementById('chainMonitorList');
    if (!monitorList) return;
    
    const monitors = highValueItems
        .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
        .slice(0, 5);
    
    if (monitors.length === 0) {
        monitorList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px; font-size: 12px;">暂无监控信息</p>';
        return;
    }
    
    monitorList.innerHTML = monitors.map(item => {
        const timeAgo = getTimeAgo(item.created_at);
        return `
            <div class="monitor-item" onclick="viewIntelligence(${item.id})">
                <div class="monitor-time">${timeAgo}</div>
                <div class="monitor-content">${escapeHtml(item.title.substring(0, 60))}${item.title.length > 60 ? '...' : ''}</div>
            </div>
        `;
    }).join('');
}

// 更新右侧快讯列表
function updateRightNewsList(newsItems) {
    const rightNewsList = document.getElementById('rightNewsList');
    if (!rightNewsList) return;
    
    if (newsItems.length === 0) {
        rightNewsList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px; font-size: 12px;">暂无快讯</p>';
        return;
    }
    
    rightNewsList.innerHTML = newsItems.map(item => {
        const timeAgo = getTimeAgo(item.created_at);
        return `
            <div class="news-item-compact" onclick="viewIntelligence(${item.id})">
                <div class="news-item-compact-title">${escapeHtml(item.title.substring(0, 50))}${item.title.length > 50 ? '...' : ''}</div>
                <div class="news-item-compact-time">${timeAgo}</div>
            </div>
        `;
    }).join('');
}

// 查看情报详情
function viewIntelligence(id) {
    const item = allIntelligence.find(i => i.id === id);
    if (item) {
        editIntelligence(id);
    }
}

// 更新热门情报
function updateHotIntelligence(intelligenceList) {
    const hotList = document.getElementById('hotIntelligenceList');
    if (!hotList) return;
    
    // 按热度和评级排序
    const hot = intelligenceList
        .map(item => {
            const score = (item.rating || 0) * 10 + (item.status === 'published' ? 5 : 0);
            return { ...item, score };
        })
        .sort((a, b) => b.score - a.score)
        .slice(0, 5);
    
    if (hot.length === 0) {
        hotList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px; font-size: 12px;">暂无热门情报</p>';
        return;
    }
    
    hotList.innerHTML = hot.map((item, index) => {
        const timeAgo = getTimeAgo(item.created_at);
        return `
            <div class="hot-item" data-rank="${index + 1}" onclick="viewIntelligence(${item.id})">
                <div class="hot-item-title">${escapeHtml(item.title.substring(0, 40))}${item.title.length > 40 ? '...' : ''}</div>
                <div class="hot-item-meta">
                    <span><i class="fas fa-star"></i> ${item.rating || 0}星</span>
                    <span><i class="fas fa-clock"></i> ${timeAgo}</span>
                </div>
            </div>
        `;
    }).join('');
}

// 更新融资动向
function updateFundingList(intelligenceList) {
    const fundingList = document.getElementById('fundingList');
    if (!fundingList) return;
    
    // 筛选包含融资相关信息的情报
    const funding = intelligenceList
        .filter(item => {
            const text = (item.title + ' ' + item.content).toLowerCase();
            return text.includes('融资') || text.includes('funding') || text.includes('投资') || text.includes('轮');
        })
        .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
        .slice(0, 5);
    
    if (funding.length === 0) {
        // 如果没有融资信息，显示高价值情报作为替代
        const alternative = intelligenceList
            .filter(item => (item.rating || 0) >= 4)
            .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
            .slice(0, 5);
        
        if (alternative.length === 0) {
            fundingList.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px; font-size: 12px;">暂无融资信息</p>';
            return;
        }
        
        fundingList.innerHTML = alternative.map(item => {
            const amount = item.rating === 5 ? '高价值' : '重要';
            return `
                <div class="funding-item" onclick="viewIntelligence(${item.id})">
                    <div class="funding-header">
                        <div class="funding-name">${escapeHtml(item.title.substring(0, 20))}${item.title.length > 20 ? '...' : ''}</div>
                        <div class="funding-amount">${amount}</div>
                    </div>
                    <div class="funding-desc">${escapeHtml(item.content.substring(0, 50))}${item.content.length > 50 ? '...' : ''}</div>
                </div>
            `;
        }).join('');
        return;
    }
    
    fundingList.innerHTML = funding.map(item => {
        // 尝试从内容中提取金额
        const content = item.content;
        const amountMatch = content.match(/(\d+[万千亿]?[美元]?)/);
        const amount = amountMatch ? amountMatch[1] : '未披露';
        
        return `
            <div class="funding-item" onclick="viewIntelligence(${item.id})">
                <div class="funding-header">
                    <div class="funding-name">${escapeHtml(item.title.substring(0, 20))}${item.title.length > 20 ? '...' : ''}</div>
                    <div class="funding-amount">${amount}</div>
                </div>
                <div class="funding-desc">${escapeHtml(item.content.substring(0, 50))}${item.content.length > 50 ? '...' : ''}</div>
            </div>
        `;
    }).join('');
}

// 点击模态框外部关闭
document.getElementById('createModal')?.addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});
