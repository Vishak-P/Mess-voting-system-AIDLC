/**
 * Admin Panel — menu management, user management, copy last week, CSV export.
 */
import React, { useEffect, useState, useCallback } from "react";
import api from "../utils/api";
import { getErrorMessage, formatDate, getMealIcon, capitalize } from "../utils/helpers";
import { CardLoader, Spinner } from "../components/Loader";
import toast from "react-hot-toast";
import {
  FiPlus, FiTrash2, FiEdit2, FiLock, FiDownload,
  FiX, FiCheck, FiCopy, FiUsers,
} from "react-icons/fi";

// ---- Create/Edit Menu Modal ----
const MenuFormModal = ({ menu, onClose, onSave }) => {
  const isEdit = !!menu;
  const [form, setForm] = useState({
    date: menu?.date || "",
    meal_type: menu?.meal_type || "breakfast",
    open_time: menu?.open_time ? menu.open_time.slice(0, 16) : "",
    deadline: menu?.deadline ? menu.deadline.slice(0, 16) : "",
    options: menu?.options?.map((o) => o.dish_name) || ["", "", ""],
  });
  const [saving, setSaving] = useState(false);

  const setOption = (i, val) => {
    const opts = [...form.options];
    opts[i] = val;
    setForm({ ...form, options: opts });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const cleanOptions = form.options.map((o) => o.trim()).filter(Boolean);
    if (cleanOptions.length < 2) { toast.error("Add at least 2 dish options"); return; }
    if (!form.date || !form.open_time || !form.deadline) {
      toast.error("Date, open time, and deadline are required"); return;
    }
    setSaving(true);
    try {
      const payload = {
        ...form,
        options: cleanOptions,
        open_time: new Date(form.open_time).toISOString(),
        deadline: new Date(form.deadline).toISOString(),
      };
      if (isEdit) {
        await api.put(`/admin/menu/${menu.id}`, payload);
        toast.success("Menu updated");
      } else {
        await api.post("/admin/create-menu", payload);
        toast.success("Menu created");
      }
      onSave();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg my-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900">
            {isEdit ? "Edit Menu" : "Create New Menu"}
          </h2>
          <button onClick={onClose} className="p-2 rounded-lg text-gray-400 hover:bg-gray-100">
            <FiX size={18} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="label">Date</label>
              <input type="date" className="input" value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })} required
                data-testid="menu-form-date" />
            </div>
            <div>
              <label className="label">Meal Type</label>
              <select className="input" value={form.meal_type}
                onChange={(e) => setForm({ ...form, meal_type: e.target.value })}
                data-testid="menu-form-meal-type">
                <option value="breakfast">🌅 Breakfast</option>
                <option value="lunch">☀️ Lunch</option>
                <option value="dinner">🌙 Dinner</option>
              </select>
            </div>
          </div>
          <div>
            <label className="label">Voting Opens</label>
            <input type="datetime-local" className="input" value={form.open_time}
              onChange={(e) => setForm({ ...form, open_time: e.target.value })} required
              data-testid="menu-form-open-time" />
          </div>
          <div>
            <label className="label">Voting Deadline</label>
            <input type="datetime-local" className="input" value={form.deadline}
              onChange={(e) => setForm({ ...form, deadline: e.target.value })} required
              data-testid="menu-form-deadline" />
          </div>
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="label mb-0">Dish Options ({form.options.length}/10)</label>
              {form.options.length < 10 && (
                <button type="button"
                  onClick={() => setForm({ ...form, options: [...form.options, ""] })}
                  className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1">
                  <FiPlus size={12} /> Add option
                </button>
              )}
            </div>
            <div className="space-y-2">
              {form.options.map((opt, i) => (
                <div key={i} className="flex gap-2">
                  <input type="text" className="input" placeholder={`Dish ${i + 1}`}
                    value={opt} onChange={(e) => setOption(i, e.target.value)}
                    data-testid={`menu-form-option-${i}`} />
                  {form.options.length > 2 && (
                    <button type="button"
                      onClick={() => setForm({ ...form, options: form.options.filter((_, idx) => idx !== i) })}
                      className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg">
                      <FiX size={14} />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="btn-secondary flex-1">Cancel</button>
            <button type="submit" disabled={saving}
              className="btn-primary flex-1 flex items-center justify-center gap-2"
              data-testid="menu-form-submit">
              {saving ? <><Spinner size="sm" /> Saving...</> : <><FiCheck size={14} /> {isEdit ? "Update" : "Create"}</>}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// ---- Export Modal ----
const ExportModal = ({ onClose }) => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [exporting, setExporting] = useState(false);

  const handleExport = async () => {
    setExporting(true);
    try {
      const params = new URLSearchParams();
      if (startDate) params.append("start_date", startDate);
      if (endDate) params.append("end_date", endDate);
      const response = await api.get(`/export/results?${params}`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      const suffix = startDate || endDate ? `_${startDate || "all"}_${endDate || "all"}` : "";
      a.download = `voting_results${suffix}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
      toast.success("CSV exported");
      onClose();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Export Results</h2>
          <button onClick={onClose} className="p-2 rounded-lg text-gray-400 hover:bg-gray-100"><FiX size={18} /></button>
        </div>
        <p className="text-sm text-gray-500 mb-4">Leave dates empty to export all results.</p>
        <div className="space-y-3 mb-4">
          <div>
            <label className="label">Start Date</label>
            <input type="date" className="input" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
          </div>
          <div>
            <label className="label">End Date</label>
            <input type="date" className="input" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
          </div>
        </div>
        <div className="flex gap-3">
          <button onClick={onClose} className="btn-secondary flex-1">Cancel</button>
          <button onClick={handleExport} disabled={exporting}
            className="btn-primary flex-1 flex items-center justify-center gap-2">
            {exporting ? <><Spinner size="sm" /> Exporting...</> : <><FiDownload size={14} /> Export CSV</>}
          </button>
        </div>
      </div>
    </div>
  );
};

// ---- Users Tab ----
const UsersTab = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(null);

  useEffect(() => {
    api.get("/admin/users").then(({ data }) => setUsers(data.users))
      .catch((err) => toast.error(getErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  const handleRoleChange = async (userId, newRole) => {
    setUpdating(userId);
    try {
      const { data } = await api.put(`/admin/users/${userId}/role`, { role: newRole });
      setUsers((prev) => prev.map((u) => u.id === userId ? data.user : u));
      toast.success(`Role updated to ${newRole}`);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setUpdating(null);
    }
  };

  if (loading) return <CardLoader count={3} />;

  return (
    <div className="card overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left py-3 px-4 text-gray-600 font-medium">Name</th>
              <th className="text-left py-3 px-4 text-gray-600 font-medium">Email</th>
              <th className="text-left py-3 px-4 text-gray-600 font-medium">Role</th>
              <th className="text-right py-3 px-4 text-gray-600 font-medium">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="py-3 px-4 font-medium text-gray-900">{user.name}</td>
                <td className="py-3 px-4 text-gray-600">{user.email}</td>
                <td className="py-3 px-4">
                  <span className={`badge ${user.role === "admin" ? "bg-purple-100 text-purple-700" : "bg-blue-100 text-blue-700"}`}>
                    {user.role}
                  </span>
                </td>
                <td className="py-3 px-4 text-right">
                  {updating === user.id ? (
                    <Spinner size="sm" />
                  ) : (
                    <button
                      onClick={() => handleRoleChange(user.id, user.role === "admin" ? "student" : "admin")}
                      className="text-xs text-blue-600 hover:text-blue-800 font-medium"
                      data-testid={`user-role-toggle-${user.id}`}>
                      Make {user.role === "admin" ? "Student" : "Admin"}
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// ---- Main Admin Panel ----
const AdminPanel = () => {
  const [menus, setMenus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("menus");
  const [modalMenu, setModalMenu] = useState(undefined);
  const [showExport, setShowExport] = useState(false);
  const [deleting, setDeleting] = useState(null);
  const [locking, setLocking] = useState(null);
  const [copying, setCopying] = useState(false);

  const fetchMenus = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/menus");
      setMenus([...data.menus].reverse());
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchMenus(); }, [fetchMenus]);

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this menu and all its votes?")) return;
    setDeleting(id);
    try {
      await api.delete(`/admin/menu/${id}`);
      toast.success("Menu deleted");
      fetchMenus();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setDeleting(null);
    }
  };

  const handleLock = async (id) => {
    setLocking(id);
    try {
      await api.post(`/admin/menu/${id}/lock`);
      toast.success("Voting locked");
      fetchMenus();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLocking(null);
    }
  };

  const handleCopyLastWeek = async () => {
    if (!window.confirm("Copy last week's menus to this week?")) return;
    setCopying(true);
    try {
      const { data } = await api.post("/admin/copy-last-week");
      toast.success(data.message);
      fetchMenus();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setCopying(false);
    }
  };

  const tabs = [
    { id: "menus", label: "Menus" },
    { id: "users", label: "Users", icon: <FiUsers size={14} /> },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Admin Panel</h1>
          <p className="text-gray-500 text-sm mt-1">Manage menus, users, and voting</p>
        </div>
        <div className="flex gap-2 flex-wrap justify-end">
          <button onClick={handleCopyLastWeek} disabled={copying}
            className="btn-secondary flex items-center gap-2 text-sm">
            {copying ? <Spinner size="sm" /> : <FiCopy size={14} />}
            Copy Last Week
          </button>
          <button onClick={() => setShowExport(true)}
            className="btn-secondary flex items-center gap-2 text-sm">
            <FiDownload size={14} /> Export CSV
          </button>
          <button onClick={() => setModalMenu(null)}
            className="btn-primary flex items-center gap-2 text-sm"
            data-testid="create-menu-button">
            <FiPlus size={14} /> Create Menu
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 border-b border-gray-200">
        {tabs.map((tab) => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}>
            {tab.icon}{tab.label}
          </button>
        ))}
      </div>

      {/* Menus tab */}
      {activeTab === "menus" && (
        loading ? <CardLoader count={4} /> : (
          <div className="card overflow-hidden p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left py-3 px-4 text-gray-600 font-medium">Date</th>
                    <th className="text-left py-3 px-4 text-gray-600 font-medium">Meal</th>
                    <th className="text-left py-3 px-4 text-gray-600 font-medium">Options</th>
                    <th className="text-left py-3 px-4 text-gray-600 font-medium">Opens</th>
                    <th className="text-left py-3 px-4 text-gray-600 font-medium">Deadline</th>
                    <th className="text-left py-3 px-4 text-gray-600 font-medium">Status</th>
                    <th className="text-right py-3 px-4 text-gray-600 font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {menus.map((menu) => (
                    <tr key={menu.id} className="hover:bg-gray-50 transition-colors">
                      <td className="py-3 px-4 font-medium text-gray-900">
                        {formatDate(menu.date, "MMM d, yyyy")}
                      </td>
                      <td className="py-3 px-4">
                        <span className="flex items-center gap-1.5">
                          {getMealIcon(menu.meal_type)}
                          <span className="capitalize text-gray-700">{menu.meal_type}</span>
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600">{menu.options?.length || 0} dishes</td>
                      <td className="py-3 px-4 text-gray-600">{formatDate(menu.open_time, "h:mm a")}</td>
                      <td className="py-3 px-4 text-gray-600">{formatDate(menu.deadline, "MMM d, h:mm a")}</td>
                      <td className="py-3 px-4">
                        {menu.is_locked ? (
                          <span className="badge bg-red-100 text-red-700">Locked</span>
                        ) : menu.voting_open ? (
                          <span className="badge bg-green-100 text-green-700">Open</span>
                        ) : (
                          <span className="badge bg-gray-100 text-gray-600">Closed</span>
                        )}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center justify-end gap-1">
                          {!menu.is_locked && (
                            <button onClick={() => handleLock(menu.id)} disabled={locking === menu.id}
                              className="p-1.5 text-amber-600 hover:bg-amber-50 rounded-lg" title="Lock voting">
                              {locking === menu.id ? <Spinner size="sm" /> : <FiLock size={14} />}
                            </button>
                          )}
                          <button onClick={() => setModalMenu(menu)}
                            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg" title="Edit">
                            <FiEdit2 size={14} />
                          </button>
                          <button onClick={() => handleDelete(menu.id)} disabled={deleting === menu.id}
                            className="p-1.5 text-red-500 hover:bg-red-50 rounded-lg" title="Delete"
                            data-testid={`delete-menu-${menu.id}`}>
                            {deleting === menu.id ? <Spinner size="sm" /> : <FiTrash2 size={14} />}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {menus.length === 0 && (
                    <tr>
                      <td colSpan={7} className="py-12 text-center text-gray-500">
                        No menus yet. Create one to get started.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )
      )}

      {/* Users tab */}
      {activeTab === "users" && <UsersTab />}

      {/* Modals */}
      {modalMenu !== undefined && (
        <MenuFormModal
          menu={modalMenu}
          onClose={() => setModalMenu(undefined)}
          onSave={() => { setModalMenu(undefined); fetchMenus(); }}
        />
      )}
      {showExport && <ExportModal onClose={() => setShowExport(false)} />}
    </div>
  );
};

export default AdminPanel;
